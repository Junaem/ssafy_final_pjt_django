# Generated by Django 3.2.6 on 2021-11-17 12:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('overview', models.TextField()),
                ('adult', models.BooleanField(default=False)),
                ('vote_average', models.FloatField()),
                ('popularity', models.FloatField()),
                ('release_date', models.DateField()),
                ('poster_path', models.CharField(max_length=200)),
                ('like_users', models.ManyToManyField(related_name='like_movies', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
