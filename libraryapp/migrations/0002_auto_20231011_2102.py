# Generated by Django 2.2 on 2023-10-11 15:32

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import libraryapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('d_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Department Id')),
                ('department', models.CharField(max_length=50, verbose_name='Department')),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('p_id', models.AutoField(primary_key=True, serialize=False)),
                ('program', models.CharField(max_length=50, verbose_name='Program')),
                ('d_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libraryapp.Department')),
            ],
        ),
        migrations.CreateModel(
            name='Studentreg',
            fields=[
                ('student_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Student Id')),
                ('student_name', models.CharField(max_length=25, validators=[django.core.validators.RegexValidator('^[A-Z][a-zA-Z\\s]*$', message='Name should start with a capital letter')], verbose_name='Student Name')),
                ('dob', models.DateField(validators=[libraryapp.models.validate_age], verbose_name='Date Of Birth')),
                ('address', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[A-Z][a-zA-Z\\s]*$', message='Address should start with a capital letter')], verbose_name='Address')),
                ('phone_number', models.CharField(default='+91', max_length=12, validators=[django.core.validators.RegexValidator(message="Phone number must start with '+91' followed by 10 digits.", regex='^\\+91\\d{10}$'), libraryapp.models.validate_phone_number], verbose_name='Phone Number')),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator(message='Invalid email format.')], verbose_name='Email')),
                ('pwd', models.CharField(max_length=25, validators=[libraryapp.models.validate_password, django.core.validators.RegexValidator(message='Password must be at least 8 characters long.', regex='^.{8,}$')], verbose_name='Password')),
                ('pic', models.ImageField(upload_to='images/', validators=[libraryapp.models.validate_image_extension], verbose_name='Profile Picture')),
                ('d_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libraryapp.Department')),
                ('p_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libraryapp.Program')),
            ],
        ),
        migrations.DeleteModel(
            name='Registration',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]