# Generated by Django 5.0.6 on 2024-05-20 08:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('locality', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('mobile', models.IntegerField(default=0)),
                ('zipcode', models.IntegerField()),
                ('state', models.CharField(choices=[('Bujumbura Mairie', 'Bujumbura Mairie'), ('Ruyigi', 'Ruyigi'), ('Ngozi', 'Ngozi'), ('Kirundo', 'Kirundo'), ('Gitega', 'Gitega'), ('Karuzi', 'Karuzi'), ('Rutana', 'Rutana'), ('Bujumbura Rural', 'Bujumbura Rural'), ('Muleba', 'Muleba'), ('Muleba', 'Muleba'), ('Muleba', 'Muleba'), ('Nairobi', 'Nairobi'), ('Mombasa', 'Mombasa'), ('Kisumu', 'Kisumu'), ('Nakuru', 'Nakuru'), ('Eldoret', 'Eldoret'), ('Thika', 'Thika'), ('Malindi', 'Malindi'), ('Kitale', 'Kitale'), ('Garissa', 'Garissa')], max_length=200)),
                ('reg_date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
