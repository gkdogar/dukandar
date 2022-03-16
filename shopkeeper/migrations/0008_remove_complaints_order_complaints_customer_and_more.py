# Generated by Django 4.0.1 on 2022-03-15 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopkeeper', '0007_rename_complaint_complaints'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='complaints',
            name='order',
        ),
        migrations.AddField(
            model_name='complaints',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shopkeeper.customer'),
        ),
        migrations.AlterField(
            model_name='complaints',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shopkeeper.employee'),
        ),
        migrations.AlterField(
            model_name='complaints',
            name='shopkeeper',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shopkeeper.shopkeeper'),
        ),
    ]
