# Generated by Django 5.0.2 on 2024-03-05 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_artiste_delete_annonce'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artiste',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='artiste',
            name='profession',
            field=models.TextField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='artiste',
            name='preuve',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
