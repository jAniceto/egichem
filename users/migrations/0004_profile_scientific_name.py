# Generated by Django 2.1.4 on 2019-01-02 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190102_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='scientific_name',
            field=models.CharField(default='J Pedro', max_length=200),
            preserve_default=False,
        ),
    ]
