from django.contrib import admin
from .models import Habit, HabitEntry

# Register your models here.

admin.site.register(Habit)
admin.site.register(HabitEntry)