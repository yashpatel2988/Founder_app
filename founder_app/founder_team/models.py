from django.db import models
from videos.models import FounderDaftar

# Create your models here.
class FounderTeamsProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    daftar = models.ForeignKey(FounderDaftar, models.DO_NOTHING)
    team_email = models.CharField(max_length=50)
    last_updated_date = models.DateField(blank=True, null=True,auto_now=True)
    last_updated_by = models.BigIntegerField(blank=True, null=True)
    created_date = models.DateField(blank=True, null=True,auto_now_add=True)
    creaed_by = models.BigIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15)
    designation = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    invitation_token = models.TextField()

    class Meta:
        managed = False
        db_table = 'founder_teams_profile'
        unique_together = (('daftar', 'team_email'),)