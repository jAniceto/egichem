# Generated by Django 2.1.4 on 2019-01-16 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0022_award'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('filetype', models.CharField(blank=True, max_length=250)),
                ('description', models.TextField(blank=True)),
                ('link', models.URLField(blank=True)),
                ('photo', models.ImageField(default='tools/tools-placeholder.png', upload_to='tools/')),
                ('program_file', models.FileField(blank=True, upload_to='tools/')),
                ('help_file', models.FileField(blank=True, upload_to='tools/')),
            ],
        ),
    ]