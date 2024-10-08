# Generated by Django 5.0.7 on 2024-07-30 16:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0003_alter_video_table'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Daftar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('daftar_name', models.CharField(max_length=255)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL)),
                ('last_updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updated_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CreatePitch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('red_flag', models.BooleanField(default=False)),
                ('reason', models.TextField(blank=True, null=True)),
                ('selection_status', models.CharField(max_length=50)),
                ('seen_status', models.BooleanField(default=False)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pitch_created_by', to=settings.AUTH_USER_MODEL)),
                ('last_updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pitch_updated_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('daftar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videos.daftar')),
            ],
        ),
        migrations.CreateModel(
            name='PitchVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_id', models.IntegerField()),
                ('question_language', models.CharField(max_length=50)),
                ('question_url', models.CharField(max_length=255)),
                ('last_updated_date', models.DateTimeField(auto_now=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_created_by', to=settings.AUTH_USER_MODEL)),
                ('last_updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_updated_by', to=settings.AUTH_USER_MODEL)),
                ('pitch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videos.createpitch')),
            ],
        ),
        migrations.DeleteModel(
            name='Video',
        ),
    ]
