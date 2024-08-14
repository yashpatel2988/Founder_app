import os
import subprocess
from django.http import JsonResponse, FileResponse
from django.shortcuts import render
#from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
#from google.cloud import speech_v1p1beta1 as speech
#from google.cloud import storage
#from google.cloud import translate_v2 as translate
#from .models import Video
#from io import BytesIO
from datetime import datetime 
from django.conf import settings
from django.core.files.storage import default_storage

def convert_video(input_file_path, size=5):
    try:
        if not os.path.exists(input_file_path):
            raise Exception("Input file does not exist.")

        os.chmod(input_file_path, 0o644)

        duration_cmd = [
            'ffprobe', '-i', input_file_path, '-show_entries', 'format=duration', 
            '-v', 'quiet', '-of', 'csv=p=0'
        ]
        try:
            duration_result = subprocess.check_output(duration_cmd).decode('utf-8').strip()
        except subprocess.CalledProcessError as e:
            raise Exception(f"ffprobe failed: {e}")

        if not duration_result:
            raise Exception("Failed to get video duration.")
        duration = float(duration_result)

        target_bitrate = int((size * 8 * 1024 * 1024) / (duration * 1000))

        output_file = f'/tmp/output_video_{size}MB.mp4'
        ffmpeg_cmd = [
            'ffmpeg', '-i', input_file_path,
            '-vf', 'scale=-2:480',
            '-b:v', f'{target_bitrate}k',
            '-maxrate', f'{target_bitrate}k',
            '-bufsize', f'{2*target_bitrate}k',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-af', 'anlmdn',
            output_file
        ]
        subprocess.run(ffmpeg_cmd, check=True)

        with open(output_file, 'rb') as f:
            converted_video_data = f.read()

        os.remove(output_file)

        return converted_video_data

    except subprocess.CalledProcessError as e:
        raise Exception(f"Conversion failed: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}")
    

#def upload_video(request):
    if request.method == 'POST':
        if 'video' not in request.FILES:
            return JsonResponse({"error": "No video file part"}, status=400)

        file = request.FILES['video']
        if not file.name:
            return JsonResponse({"error": "No selected video file"}, status=400)

        try:
            input_path = default_storage.save(f'tmp/{file.name}', file)
            input_path = os.path.join(settings.MEDIA_ROOT, input_path)

            #text = transcribe_video_to_text(input_path)

            converted_video_data = convert_video(input_path)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            final_folder = os.path.join(settings.MEDIA_ROOT, 'converted', timestamp)
            os.makedirs(final_folder, exist_ok=True)

            final_file_path = os.path.join(final_folder, f"converted_{file.name}")

            with open(final_file_path, 'wb') as f:
                f.write(converted_video_data)

            video = Video(file_path=final_file_path, upload_time=timezone.now()) #transcription=text)
            video.save()

            return JsonResponse({"message": "Video uploaded and converted successfully", "file_path": final_file_path}, status=200)

        except Exception as e:
            return JsonResponse({"error": f"Video conversion failed: {str(e)}"}, status=500)


#def watch_last_uploaded_video(request):
    last_video = Video.objects.order_by('-id').first()
    if last_video:
        if os.path.exists(last_video.file_path):
            return FileResponse(open(last_video.file_path, 'rb'), as_attachment=True)
        else:
            return JsonResponse({"error": "Video file not found"}, status=404)
    else:
        return JsonResponse({"error": "No videos uploaded yet"}, status=404)
