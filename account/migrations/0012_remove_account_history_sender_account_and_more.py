# Generated by Django 4.2.2 on 2023-07-25 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_alter_account_history_account_history_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account_history',
            name='sender_account',
        ),
        migrations.AddField(
            model_name='account_history',
            name='sender_name',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]
