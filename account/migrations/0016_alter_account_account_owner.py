# Generated by Django 4.2.2 on 2023-07-26 19:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0015_alter_account_account_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account', to=settings.AUTH_USER_MODEL),
        ),
    ]
