# Generated by Django 4.1.2 on 2022-11-05 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendar_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetings',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='meetings',
            name='title',
            field=models.CharField(default='business meeting', max_length=180),
        ),
        migrations.AlterField(
            model_name='day',
            name='count_meetings',
            field=models.IntegerField(default=0),
        ),
    ]
