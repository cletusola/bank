# Generated by Django 4.2.2 on 2023-06-22 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='account_type',
            field=models.CharField(choices=[('savings', 'savings'), ('checkings', 'checkings')], default='savings', max_length=20),
        ),
    ]
