from django.db import models

class UserProfile(models.Model):
    ROLE_CHOICES = [
        (10, 'Founder'),
        (20, 'Investor'),
    ]
    
    id = models.AutoField(primary_key=True)
    role = models.IntegerField(choices=ROLE_CHOICES)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15)
    login_id = models.EmailField(unique=True)
    language = models.CharField(max_length=20)
    last_updated_date = models.DateTimeField(auto_now=True)
    last_updated_by = models.IntegerField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_profile'  # Replace with the actual table name
        managed = False
