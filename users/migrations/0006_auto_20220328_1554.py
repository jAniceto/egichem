# Generated by Django 3.2.7 on 2022-03-28 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20220317_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='ciencia_id',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='profile',
            name='scientific_name',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]