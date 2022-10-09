# Generated by Django 4.1.1 on 2022-10-09 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='subscribechannel',
            constraint=models.UniqueConstraint(fields=('user', 'channel'), name='user_and_channel_uniq'),
        ),
    ]
