# Generated by Django 5.1.6 on 2025-02-18 00:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr_assist', '0011_remove_allowance_employee_remove_allowance_paymonth'),
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
    ]
