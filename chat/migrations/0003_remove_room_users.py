# Generated by Django 4.1.5 on 2023-03-15 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_room_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='users',
        ),
    ]
