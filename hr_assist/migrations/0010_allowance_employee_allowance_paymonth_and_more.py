# Generated by Django 5.1.6 on 2025-02-14 01:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr_assist', '0009_allowance_allowancelist'),
    ]

    operations = [
        migrations.AddField(
            model_name='allowance',
            name='employee',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='hr_assist.employee'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='allowance',
            name='paymonth',
            field=models.CharField(default=1, max_length=7),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='allowance',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
