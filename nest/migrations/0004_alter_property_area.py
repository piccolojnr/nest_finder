# Generated by Django 5.0.4 on 2024-04-08 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nest', '0003_alter_adminaction_timestamp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='area',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
