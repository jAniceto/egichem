# Generated by Django 2.2.3 on 2019-07-27 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0011_auto_20190727_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='item_type',
            field=models.CharField(choices=[('Reagent', 'Reagent'), ('Material', 'Material'), ('Tool', 'Tool'), ('Other', 'Other')], default='Reagent', max_length=50),
        ),
    ]