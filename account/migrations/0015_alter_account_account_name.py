# Generated by Django 4.2.2 on 2023-07-25 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_account_account_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_name',
            field=models.CharField(max_length=60),
        ),
    ]