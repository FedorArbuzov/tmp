# Generated by Django 3.2.11 on 2023-04-11 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_studentsgroup'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentsgroup',
            old_name='tags',
            new_name='users',
        ),
        migrations.RemoveField(
            model_name='studentsgroup',
            name='steps',
        ),
        migrations.AddField(
            model_name='studentsgroup',
            name='programs',
            field=models.ManyToManyField(blank=True, to='users.Program'),
        ),
    ]
