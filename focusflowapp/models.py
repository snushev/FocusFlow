from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Habit(models.Model):
    name = models.CharField(max_length=100)
    goal_per_day = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class HabitEntry(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='entries')
    date = models.DateField()
    completed_count = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.habit.name} on {self.date}"