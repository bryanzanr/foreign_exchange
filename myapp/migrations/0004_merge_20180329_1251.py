# Generated by Django 2.0.2 on 2018-03-29 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20180326_1303'),
        ('myapp', '0002_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='ads',
            name='address',
            field=models.CharField(
                blank=True, default=None, max_length=45, null=True),
        ),
        migrations.AddField(
            model_name='ads',
            name='latitude',
            field=models.CharField(
                blank=True, default=None, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='ads',
            name='longitude',
            field=models.CharField(
                blank=True, default=None, max_length=30, null=True),
        ),
    ]
