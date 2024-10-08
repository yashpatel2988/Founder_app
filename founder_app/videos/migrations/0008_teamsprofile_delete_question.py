# Generated by Django 5.0.7 on 2024-07-31 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0007_alter_createpitch_table_alter_daftar_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamsProfile',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('daftar_id', models.BigIntegerField()),
                ('team_email', models.CharField(max_length=50)),
                ('rowstate', models.BigIntegerField()),
                ('last_updated_date', models.DateField(blank=True, null=True)),
                ('last_updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateField(blank=True, null=True)),
                ('creaed_by', models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'teams_profile',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]
