# Generated by Django 4.0.5 on 2022-06-15 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AccountProfile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountprofile',
            name='contact',
            field=models.CharField(default='0737532340', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='accountprofile',
            name='email',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='accountprofile',
            name='identity_number',
            field=models.CharField(default='0737532340', max_length=100),
            preserve_default=False,
        ),
    ]
