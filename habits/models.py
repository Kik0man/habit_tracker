from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    place = models.CharField(max_length=255, verbose_name="Место")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.CharField(max_length=255, verbose_name="Действие")
    is_pleasant = models.BooleanField(default=False, verbose_name="Приятная привычка")
    related_habit = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='related_to', verbose_name="Связанная привычка"
    )
    periodicity = models.PositiveSmallIntegerField(
        default=1, verbose_name="Периодичность (дни)",
        help_text="Не реже 1 раза в 7 дней"
    )
    reward = models.CharField(max_length=255, blank=True, null=True, verbose_name="Вознаграждение")
    duration = models.PositiveSmallIntegerField(verbose_name="Время на выполнение (сек)")
    is_public = models.BooleanField(default=False, verbose_name="Публичная")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ['time']

    def __str__(self):
        return f"{self.user.username}: {self.action} в {self.time}"

    def clean(self):
        # 1. Нельзя одновременно указать reward и related_habit
        if self.reward and self.related_habit:
            raise ValidationError("Нельзя заполнять и вознаграждение, и связанную привычку")

        # 2. Время выполнения не больше 120 секунд
        if self.duration > 120:
            raise ValidationError("Время выполнения не должно превышать 120 секунд")

        # 3. Связанная привычка может быть только приятной
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной")

        # 4. У приятной привычки не может быть reward или related_habit
        if self.is_pleasant:
            if self.reward or self.related_habit:
                raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки")

        # 5. Периодичность не реже 1 раза в 7 дней
        if self.periodicity < 1 or self.periodicity > 7:
            raise ValidationError("Периодичность должна быть от 1 до 7 дней")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)