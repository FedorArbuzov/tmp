# Generated by Django 3.2.11 on 2023-05-16 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0032_test_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentinfo',
            name='avatar',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]