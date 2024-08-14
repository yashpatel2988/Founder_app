from django.db import models

class FounderProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15)
    login_id = models.CharField(max_length=50)
    language = models.JSONField(max_length=50)
    last_updated_date = models.DateField(blank=True, null=True,auto_now=True)
    last_updated_by = models.BigIntegerField(blank=True, null=True)
    created_date = models.DateField(blank=True, null=True,auto_now_add=True)
    created_by = models.BigIntegerField(blank=True, null=True)
    is_active = models.BooleanField(db_column='isActive',default=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'founder_profile'
        unique_together = (('phone_number', 'login_id'),)
