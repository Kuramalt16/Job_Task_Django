# Generated by Django 5.0.6 on 2024-06-11 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0003_companies_company_value'),
    ]

    operations = [
        migrations.RenameField(
            model_name='companies',
            old_name='company_value',
            new_name='company_volume',
        ),
    ]