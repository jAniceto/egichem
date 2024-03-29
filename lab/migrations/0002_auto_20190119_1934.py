# Generated by Django 2.1.4 on 2019-01-19 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='material',
            name='msds_link',
        ),
        migrations.AddField(
            model_name='material',
            name='msds_url',
            field=models.URLField(blank=True, verbose_name='MSDS URL'),
        ),
        migrations.AddField(
            model_name='material',
            name='specifications',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='material',
            name='cas',
            field=models.CharField(blank=True, max_length=50, verbose_name='CAS'),
        ),
        migrations.AlterField(
            model_name='material',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
