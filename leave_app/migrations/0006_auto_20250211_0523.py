# Generated by Django 2.2.16 on 2025-02-11 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave_app', '0005_leaverequest_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leaverequest',
            name='status',
        ),
        migrations.AddField(
            model_name='leaverequest',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
