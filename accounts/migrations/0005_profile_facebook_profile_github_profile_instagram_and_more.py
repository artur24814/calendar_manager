# Generated by Django 4.1.5 on 2023-03-13 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_profile_day_available_places_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='facebook',
            field=models.URLField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='github',
            field=models.URLField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='instagram',
            field=models.URLField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='twitter',
            field=models.URLField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='website',
            field=models.URLField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='meeting_type',
            field=models.IntegerField(choices=[(15, '15m'), (30, '30m'), (45, '45m'), (60, '1h'), (1, '1d')], default=2, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='work_regulations',
            field=models.IntegerField(choices=[(1, 'Mon-Fri'), (2, 'Mon-Sun'), (3, 'Mon-Sat'), (4, 'Sun-Sat')], default=1, null=True),
        ),
    ]
