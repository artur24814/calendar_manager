# Generated by Django 4.1.5 on 2023-03-20 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_unreadmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='unreadmessage',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
