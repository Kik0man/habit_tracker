from rest_framework import serializers
from .models import Habit

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user',)

    def validate(self, data):
        # Дополнительные валидации, не охваченные в clean() модели
        if data.get('is_pleasant') and (data.get('reward') or data.get('related_habit')):
            raise serializers.ValidationError("У приятной привычки нет вознаграждения или связанной привычки")
        if data.get('reward') and data.get('related_habit'):
            raise serializers.ValidationError("Выберите только одно: вознаграждение или связанная привычка")
        if data.get('related_habit') and not data['related_habit'].is_pleasant:
            raise serializers.ValidationError("Связанная привычка должна быть приятной")
        if data.get('duration', 0) > 120:
            raise serializers.ValidationError("Время выполнения ≤ 120 секунд")
        if data.get('periodicity', 1) > 7:
            raise serializers.ValidationError("Периодичность не может быть больше 7 дней")
        return data