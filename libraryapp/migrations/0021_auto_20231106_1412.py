# Generated by Django 2.2 on 2023-11-06 08:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0020_auto_20231106_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='callno',
            field=models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator('^[A-Za-z0-9\\-,\\s]+$', message="Call number should contain letters, digits, '-', and ','.")]),
        ),
        migrations.AlterField(
            model_name='staffreg',
            name='pwd',
            field=models.CharField(default='ADXg5LshL0sy', max_length=25, verbose_name='Password'),
        ),
        migrations.AlterField(
            model_name='studentreg',
            name='pwd',
            field=models.CharField(default='3czUTERVOOK0', max_length=25, verbose_name='Password'),
        ),
    ]