# Generated by Django 3.2.6 on 2021-11-19 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='poster_path',
            field=models.CharField(max_length=100),
        ),
    ]
