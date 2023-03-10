# Generated by Django 4.1.5 on 2023-01-12 18:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='moviebooking',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='moviebooking',
            name='status',
            field=models.CharField(choices=[('CONFIRMED', 'Confirmed'), ('CANCELLED', 'Cancelled')], default='CONFIRMED', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='moviebooking',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
