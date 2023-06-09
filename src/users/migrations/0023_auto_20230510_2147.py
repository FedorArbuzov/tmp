# Generated by Django 3.2.11 on 2023-05-10 21:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_useranswer_html'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useranswer',
            name='answers',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='useranswer',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.course'),
        ),
        migrations.AlterField(
            model_name='useranswer',
            name='html',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.htmlpage'),
        ),
        migrations.AlterField(
            model_name='useranswer',
            name='lesson',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.lesson'),
        ),
        migrations.AlterField(
            model_name='useranswer',
            name='test',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.test'),
        ),
        migrations.AlterField(
            model_name='useranswer',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.topic'),
        ),
    ]
