# Generated by Django 3.2.11 on 2023-04-11 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20230411_0656'),
    ]

    operations = [
        migrations.AddField(
            model_name='step',
            name='name',
            field=models.CharField(default='', max_length=300),
        ),
    ]
