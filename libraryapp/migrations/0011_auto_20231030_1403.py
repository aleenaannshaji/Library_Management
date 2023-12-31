# Generated by Django 2.2 on 2023-10-30 08:33

import django.core.validators
from django.db import migrations, models
import libraryapp.models
import libraryapp.validators


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0010_auto_20231028_2353'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accno', models.CharField(editable=False, max_length=6, unique=True)),
                ('callno', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator('^[A-Za-z0-9\\-\\s]+$')])),
                ('title', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator('^[A-Z][a-zA-Z\\s]+$')])),
                ('author', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator('^[A-Za-z\\s]+$')])),
                ('year_of_published', models.PositiveIntegerField(validators=[libraryapp.models.validate_year_of_published])),
                ('isbn', models.CharField(max_length=12, validators=[libraryapp.models.validate_isbn])),
                ('publisher', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[A-Za-z\\s]+$')])),
                ('pages', models.PositiveIntegerField()),
                ('type_of_book', models.CharField(choices=[('Fiction', 'Fiction'), ('Non-Fiction', 'Non-Fiction'), ('Science', 'Science'), ('Biography', 'Biography')], max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='staffreg',
            name='pwd',
            field=models.CharField(default='I7lemY4CiFNN', max_length=25, verbose_name='Password'),
        ),
        migrations.AlterField(
            model_name='studentreg',
            name='dob',
            field=models.DateField(blank=True, null=True, validators=[libraryapp.validators.YourAgeValidator], verbose_name='Date Of Birth'),
        ),
        migrations.AlterField(
            model_name='studentreg',
            name='pwd',
            field=models.CharField(default='LDG9W9bkpdQk', max_length=25, verbose_name='Password'),
        ),
    ]
