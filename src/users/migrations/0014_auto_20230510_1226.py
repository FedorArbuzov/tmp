# Generated by Django 3.2.11 on 2023-05-10 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20230510_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='weight',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='weight',
            field=models.IntegerField(default=0),
        ),
    ]
