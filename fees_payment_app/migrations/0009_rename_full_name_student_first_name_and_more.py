# Generated by Django 4.2.13 on 2024-07-06 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fees_payment_app', '0008_remove_fee_facaulty_remove_fee_level_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='full_name',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='student',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
