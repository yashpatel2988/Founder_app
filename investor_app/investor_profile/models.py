from django.db import models

# Create your models here.
class InvesterProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(db_column=' last_name', max_length=50)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    gender = models.CharField(db_column=' gender', max_length=50)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    date_of_birth = models.DateField(db_column='date_of _birth')  # Field renamed to remove unsuitable characters.
    phone_number = models.CharField(max_length=15)
    login_id = models.CharField(db_column=' login_id', max_length=50)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    email = models.CharField(max_length=50)
    last_updated_date = models.DateField(blank=True, null=True,auto_now=True)
    last_updated_by = models.BigIntegerField(blank=True, null=True)
    created_date = models.DateField(blank=True, null=True,auto_now_add=True)
    created_by = models.BigIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'invester_profile'
        unique_together = (('login_id', 'phone_number'),)
