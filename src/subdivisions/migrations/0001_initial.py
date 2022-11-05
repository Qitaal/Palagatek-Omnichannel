# Generated by Django 3.2.16 on 2022-11-04 18:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('postal_code', models.CharField(max_length=5)),
            ],
            options={
                'db_table': 'cities',
            },
        ),
        migrations.CreateModel(
            name='Provinces',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'provinces',
            },
        ),
        migrations.CreateModel(
            name='Subdistricts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('city_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subdivisions.cities')),
            ],
            options={
                'db_table': 'subdistricts',
            },
        ),
        migrations.AddField(
            model_name='cities',
            name='province_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subdivisions.provinces'),
        ),
    ]