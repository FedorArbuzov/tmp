# Generated by Django 3.2.11 on 2023-05-10 21:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_useranswer_lesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useranswer',
            name='test',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='users.test'),
        ),
    ]