# Generated by Django 3.2.11 on 2023-05-16 02:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0027_lesson_order_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswer',
            name='step',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.step'),
        ),
    ]
