# Generated by Django 3.2.7 on 2021-12-10 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0030_alter_member_position'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainResearchAreas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('order', models.IntegerField(default=99)),
            ],
        ),
    ]