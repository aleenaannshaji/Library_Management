# Generated by Django 2.2 on 2023-10-31 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0016_auto_20231031_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentreg',
            name='libno',
            field=models.CharField(default='1001', max_length=4, unique=True, verbose_name='Library Number'),
        ),
        migrations.AlterField(
            model_name='staffreg',
            name='pwd',
            field=models.CharField(default='1HOGN9VLZJeC', max_length=25, verbose_name='Password'),
        ),
        migrations.AlterField(
            model_name='studentreg',
            name='pwd',
            field=models.CharField(default='SfAODz5MGHhb', max_length=25, verbose_name='Password'),
        ),
    ]
