# Generated by Django 2.0.2 on 2018-03-26 06:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        # ('myapp', '0002_ads'),
        ('hello', '0002_ads'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='ads',
        #     name='img',
        #     field=models.CharField(
        #         blank=True, default=None, max_length=300, null=True),
        # ),
        migrations.AlterField(
            model_name='ads',
            name='published_date',
            field=models.DateTimeField(
                auto_now=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
