from django.db import models
from investor_profile.models import InvesterProfile

# Create your models here.
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
