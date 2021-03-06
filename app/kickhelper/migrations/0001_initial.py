# Generated by Django 3.0.2 on 2020-01-26 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=200)),
                ('currency', models.CharField(max_length=200)),
                ('expected_launch', models.DateField()),
                ('deadline', models.DateField()),
                ('goal', models.FloatField()),
                ('current_state', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
