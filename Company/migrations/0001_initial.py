# Generated by Django 5.0.6 on 2024-06-11 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Companies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=200)),
                ('company_symbol', models.CharField(max_length=10)),
                ('company_industry', models.CharField(max_length=100)),
                ('date', models.DateTimeField()),
            ],
        ),
    ]
