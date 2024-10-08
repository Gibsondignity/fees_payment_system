# Generated by Django 4.2.13 on 2024-06-21 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fees_payment_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fee',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fees_payment_app.student'),
        ),
        migrations.AddField(
            model_name='payment',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='ref',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.CharField(blank=True, default='pending', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='verify',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='fee',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fees_payment_app.course'),
        ),
        migrations.AlterField(
            model_name='fee',
            name='semester',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fees_payment_app.semester'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fees_payment_app.student'),
        ),
    ]
