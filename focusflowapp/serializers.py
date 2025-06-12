from rest_framework import serializers
from .models import Habit, HabitEntry

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['name', 'goal_per_day', 'created_at']
        read_only_fields = ['id', 'created_at']

class HabitEntrySerializer(serializers.ModelSerializer):
    habit = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Habit.objects.all()
    )


    class Meta:
        model = HabitEntry
        fields = ['habit', 'date', 'completed_count']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()