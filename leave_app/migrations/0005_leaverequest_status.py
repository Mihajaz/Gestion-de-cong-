# Generated by Django 2.2.16 on 2025-02-06 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave_app', '0004_auto_20250206_0634'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaverequest',
            name='status',
            field=models.CharField(choices=[('En attente', 'En attente'), ('Validé', 'Validé'), ('Refusé', 'Refusé')], default='En attente', max_length=20),
        ),
    ]
