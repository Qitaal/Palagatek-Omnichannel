# Generated by Django 3.2.16 on 2022-11-05 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20221105_1425'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='colors',
            table='product_colors',
        ),
        migrations.AlterModelTable(
            name='variants',
            table='product_variants',
        ),
    ]