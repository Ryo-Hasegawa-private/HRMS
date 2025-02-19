# Generated by Django 5.1.5 on 2025-02-10 01:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('birth_date', models.DateField()),
                ('gender', models.BooleanField()),
                ('email', models.EmailField(max_length=254)),
                ('basic_salary', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10000000)])),
                ('joining_date', models.DateField()),
            ],
        ),
    ]
