# Generated by Django 4.1.7 on 2023-03-22 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_posts'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Posts',
        ),
    ]
