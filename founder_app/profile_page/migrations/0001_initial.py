# Generated by Django 5.0.7 on 2024-07-29 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=10)),
                ('dateofbirth', models.DateField()),
                ('phoneno', models.CharField(max_length=15)),
                ('language', models.CharField(max_length=30)),
            ],
        ),
    ]
