# Generated by Django 4.2.2 on 2023-07-26 19:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0017_alter_account_account_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_account', to=settings.AUTH_USER_MODEL),
        ),
    ]
