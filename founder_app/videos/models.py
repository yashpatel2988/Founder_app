from django.db import models
from profile_page.models import FounderProfile


class FounderDaftar(models.Model):
    id = models.BigAutoField(primary_key=True)
    founder = models.ForeignKey(FounderProfile, models.DO_NOTHING)
    daftar_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    last_updated_date = models.DateField(blank=True, null=True,auto_now=True)
    last_updated_by = models.BigIntegerField(blank=True, null=True)
    created_date = models.DateField(blank=True, null=True,auto_now_add=True)
    created_by = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'founder_daftar'
        unique_together = (('founder', 'daftar_name'),)


class CreatePitch(models.Model):
    id = models.BigAutoField(primary_key=True)
    daftar = models.ForeignKey('FounderDaftar', models.DO_NOTHING)
    founder = models.ForeignKey(FounderProfile, models.DO_NOTHING)
    program = models.ForeignKey('InvesterPrograms', models.DO_NOTHING)
    red_flag = models.BooleanField(blank=True, null=True)
    reason = models.CharField(blank=True, null=True)
    last_updated_date = models.DateField(blank=True, null=True,auto_now=True)
    last_updated_by = models.BigIntegerField(blank=True, null=True)
    created_date = models.DateField(blank=True, null=True,auto_now_add=True)
    created_by = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'create_pitch'
        unique_together = (('daftar', 'program'),)

class Question(models.Model):
    id = models.BigAutoField(primary_key=True)
    question = models.CharField()
    last_updated_date = models.DateField(blank=True, null=True)
    last_updated_by = models.BigIntegerField(blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    created_by = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'question'



class PitchVideos(models.Model):
    id = models.BigAutoField(primary_key=True)
    pitch = models.ForeignKey(CreatePitch, models.DO_NOTHING)
    question = models.ForeignKey('Question', models.DO_NOTHING)
    question_language = models.CharField()
    question_url = models.TextField()
    last_updated_date = models.DateField(blank=True, null=True)
    updated_by = models.BigIntegerField(blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    created_by = models.BigIntegerField(blank=True, null=True)
    founder = models.ForeignKey(FounderProfile, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'pitch_videos'


class DaftarDetail(models.Model):
    id = models.BigAutoField(primary_key=True)
    daftar = models.ForeignKey('FounderDaftar', models.DO_NOTHING)
    founder = models.ForeignKey(FounderProfile, models.DO_NOTHING)
    sector = models.CharField()
    stage = models.CharField()
    demolink = models.TextField()
    problem_loacation = models.CharField()
    solving_your_problem = models.BooleanField()
    last_updated_date = models.DateField(blank=True, null=True)
    last_updated_by = models.BigIntegerField(blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    created_by = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'daftar_detail'


##For Refrence Only 

class Community(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(blank=True, null=True)
    last_updated_date = models.DateField(blank=True, null=True)
    last_updated_by = models.BigIntegerField(blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    created_by_field = models.BigIntegerField(db_column='created_by ', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'community'

class InvesterProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    field_last_name = models.CharField(db_column=' last_name', max_length=50)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    field_gender = models.CharField(db_column=' gender', max_length=50)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    date_of_birth = models.DateField(db_column='date_of _birth')  # Field renamed to remove unsuitable characters.
    phone_number = models.CharField(max_length=15)
    field_login_id = models.CharField(db_column=' login_id', max_length=50)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    email = models.CharField(max_length=50)
    last_updated_date = models.DateField(blank=True, null=True)
    last_updated_by = models.BigIntegerField(blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    created_by = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'invester_profile'
        unique_together = (('field_login_id', 'phone_number'),)

class Sector(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(blank=True, null=True)
    last_updated_date = models.DateField(blank=True, null=True)
    last_updated_by = models.BigIntegerField(blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    created_by_field = models.BigIntegerField(db_column='created_by ', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'sector'



class InvesterPrograms(models.Model):
    id = models.BigAutoField(primary_key=True)
    elevator_pitch = models.TextField()
    title = models.CharField(max_length=100)
    collabration = models.CharField(max_length=100)
    collabration_url = models.TextField()
    team = models.BigIntegerField()
    sector = models.ForeignKey('Sector', models.DO_NOTHING)
    capital = models.IntegerField()
    equity = models.IntegerField()
    stage = models.CharField(max_length=50)
    last_date_of_pitch = models.DateField()
    community = models.ForeignKey(Community, models.DO_NOTHING)
    location = models.CharField(max_length=50)
    age_group = models.CharField(max_length=10, blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    view = models.BooleanField()
    shared = models.BooleanField()
    last_updated_date = models.DateField(blank=True, null=True)
    last_updated_by = models.BigIntegerField(blank=True, null=True)
    created_date = models.DateField(blank=True, null=True)
    created_by = models.BigIntegerField(blank=True, null=True)
    invester = models.ForeignKey(InvesterProfile, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'invester_programs'


