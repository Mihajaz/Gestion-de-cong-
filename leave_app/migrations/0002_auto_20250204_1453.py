# Generated by Django 2.2.16 on 2025-02-04 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='nom',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='role',
        ),
        migrations.AddField(
            model_name='employee',
            name='name',
            field=models.CharField(default='Nom', max_length=50),
        ),
        migrations.AddField(
            model_name='employee',
            name='poste',
            field=models.CharField(default='Poste', max_length=100),
        ),
        migrations.AlterField(
            model_name='employee',
            name='email',
            field=models.EmailField(default='email', max_length=254),
        ),
        migrations.AlterField(
            model_name='leaverequest',
            name='reason',
            field=models.TextField(max_length=50),
        ),
    ]
