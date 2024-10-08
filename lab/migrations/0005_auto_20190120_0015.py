# Generated by Django 2.1.5 on 2019-01-20 00:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0004_auto_20190119_2329'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='material',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='material',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='material',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='material',
            name='modified',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
