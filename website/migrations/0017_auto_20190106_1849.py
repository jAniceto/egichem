# Generated by Django 2.1.4 on 2019-01-06 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0016_auto_20190106_1832'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='thesis_cooedinators',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='publication',
            name='thesis_institution',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
