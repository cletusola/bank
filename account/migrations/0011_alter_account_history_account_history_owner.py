# Generated by Django 4.2.2 on 2023-07-24 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_account_history_account_history_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account_history',
            name='account_history_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history_owner', to='account.account'),
        ),
    ]
