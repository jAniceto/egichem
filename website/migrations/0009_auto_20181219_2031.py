# Generated by Django 2.1.4 on 2018-12-19 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='position',
            field=models.CharField(choices=[('Professor', 'Professor'), ('PostDoc Researcher', 'PostDoc Researcher'), ('PhD Student', 'PhD Student'), ('Research Fellows', 'Research Fellows'), ('MSc Students', 'MSc Students'), ('Undergraduate Students', 'Undergraduate Students')], max_length=50),
        ),
    ]