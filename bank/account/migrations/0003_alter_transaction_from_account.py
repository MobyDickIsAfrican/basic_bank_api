# Generated by Django 4.0.5 on 2022-06-15 09:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='from_account',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='account.account'),
        ),
    ]