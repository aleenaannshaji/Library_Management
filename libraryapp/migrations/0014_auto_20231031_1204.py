# Generated by Django 2.2 on 2023-10-31 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libraryapp', '0013_auto_20231030_1429'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='id',
        ),
        migrations.AlterField(
            model_name='book',
            name='accno',
            field=models.CharField(editable=False, max_length=6, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='book',
            name='publisher',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='staffreg',
            name='pwd',
            field=models.CharField(default='2IoJUtthefmT', max_length=25, verbose_name='Password'),
        ),
        migrations.AlterField(
            model_name='studentreg',
            name='pwd',
            field=models.CharField(default='cfTsSCrhsc4S', max_length=25, verbose_name='Password'),
        ),
    ]
