# Generated by Django 5.0 on 2023-12-30 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='courier',
            unique_together={('first_name', 'last_name')},
        ),
    ]