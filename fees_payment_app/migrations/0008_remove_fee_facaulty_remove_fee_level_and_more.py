# Generated by Django 4.2.13 on 2024-07-06 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fees_payment_app', '0007_alter_academic_year_year_student_areas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fee',
            name='facaulty',
        ),
        migrations.RemoveField(
            model_name='fee',
            name='level',
        ),
        migrations.RemoveField(
            model_name='fee',
            name='percentage',
        ),
        migrations.RemoveField(
            model_name='fee',
            name='student_category',
        ),
        migrations.DeleteModel(
            name='Student_Areas',
        ),
    ]
