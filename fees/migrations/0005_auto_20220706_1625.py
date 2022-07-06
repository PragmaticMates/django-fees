# Generated by Django 3.1.14 on 2022-07-06 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0004_auto_20220412_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='is_fallback',
            field=models.BooleanField(db_index=True, default=False, help_text='Fallback package for purchaser when its subscription expires or trial ends (useful for freemium packages). Only 1 fallback package at a time can be set.'),
        ),
        migrations.AlterField(
            model_name='package',
            name='is_default',
            field=models.BooleanField(db_index=True, default=False, help_text='Default package for new purchaser (useful for trial packages). Only 1 default package at a time can be set.'),
        ),
    ]
