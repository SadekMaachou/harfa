# Generated by Django 5.0.2 on 2024-03-16 02:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_remove_artiste_phone_number_artiste_profession_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Annonce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200)),
                ('description', models.TextField(default='no description')),
                ('likes', models.IntegerField(blank=True, default=0, null=True)),
                ('photo1', models.ImageField(blank=True, null=True, upload_to='images_annonce/')),
                ('photo2', models.ImageField(blank=True, null=True, upload_to='images_annonce/')),
                ('photo3', models.ImageField(blank=True, null=True, upload_to='images_annonce/')),
            ],
        ),
        migrations.AlterField(
            model_name='artiste',
            name='profession',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('annonce', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='client.annonce')),
                ('commenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('description', models.TextField(default='no description')),
                ('price', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('published_date', models.DateTimeField(auto_now_add=True)),
                ('photo1', models.ImageField(blank=True, null=True, upload_to='images_products/')),
                ('photo2', models.ImageField(blank=True, null=True, upload_to='images_products/')),
                ('photo3', models.ImageField(blank=True, null=True, upload_to='images_products/')),
                ('prodect_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
