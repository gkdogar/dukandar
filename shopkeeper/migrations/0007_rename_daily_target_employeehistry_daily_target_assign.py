# Generated by Django 4.0.1 on 2022-03-04 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopkeeper', '0006_alter_employee_updated_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employeehistry',
            old_name='daily_target',
            new_name='daily_target_assign',
        ),
    ]
