# Generated by Django 5.1.5 on 2025-02-10 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr_assist', '0002_remove_employee_name_employee_mei_employee_sei_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='id',
        ),
        migrations.AddField(
            model_name='employee',
            name='emp_id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
