from django.contrib import admin

from habits.models import PlanHabit, Habit

admin.site.register(Habit)
admin.site.register(PlanHabit)
