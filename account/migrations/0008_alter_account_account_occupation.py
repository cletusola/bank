# Generated by Django 4.2.2 on 2023-06-22 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_account_account_occupation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_occupation',
            field=models.CharField(max_length=60),
        ),
    ]
