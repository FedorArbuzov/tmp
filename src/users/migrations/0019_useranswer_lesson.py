# Generated by Django 3.2.11 on 2023-05-10 21:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_auto_20230510_2131'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswer',
            name='lesson',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='users.lesson'),
            preserve_default=False,
        ),
    ]
