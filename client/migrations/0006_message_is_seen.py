# Generated by Django 5.0.2 on 2024-03-22 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0005_conversation_message_panier'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_seen',
            field=models.BooleanField(default=False),
        ),
    ]
