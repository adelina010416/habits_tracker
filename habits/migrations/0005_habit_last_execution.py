# Generated by Django 5.0.4 on 2024-04-13 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0004_alter_habit_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='habit',
            name='last_execution',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='оследнее выполнение'),
        ),
    ]
