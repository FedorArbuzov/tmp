# Generated by Django 3.2.11 on 2023-05-04 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_rename_programs_studentsgroup_courses'),
    ]

    operations = [
        migrations.AddField(
            model_name='step',
            name='lesson',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='users.lesson'),
        ),
        migrations.DeleteModel(
            name='Program',
        ),
    ]