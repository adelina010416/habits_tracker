# Generated by Django 5.0.4 on 2024-04-13 22:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0005_habit_last_execution'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanHabit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField(verbose_name='время')),
                ('today_habit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='habits.habit', verbose_name='сегодняшняя привычка')),
            ],
            options={
                'verbose_name': 'Привычка на сегодня',
                'verbose_name_plural': 'Привычки на сегодня',
            },
        ),
    ]