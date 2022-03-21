# Generated by Django 4.0 on 2022-03-08 00:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_alter_user_followers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='following', related_query_name='following', to=settings.AUTH_USER_MODEL),
        ),
    ]
