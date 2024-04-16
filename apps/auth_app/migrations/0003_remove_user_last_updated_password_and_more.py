# Generated by Django 5.0.3 on 2024-04-16 07:24

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth_app", "0002_user_email_verified_at"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="last_updated_password",
        ),
        migrations.AddField(
            model_name="user",
            name="password_last_updated",
            field=models.DateTimeField(
                blank=True, default=django.utils.timezone.now, null=True
            ),
        ),
    ]