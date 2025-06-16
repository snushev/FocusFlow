from rest_framework import serializers
from .models import Habit, HabitEntry
from django.contrib.auth.models import User

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'name', 'goal_per_day', 'created_at']
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

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )