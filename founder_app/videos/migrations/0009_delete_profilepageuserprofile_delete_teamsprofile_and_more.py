# Generated by Django 5.0.7 on 2024-08-07 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0008_teamsprofile_delete_question'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProfilePageUserprofile',
        ),
        migrations.DeleteModel(
            name='TeamsProfile',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
