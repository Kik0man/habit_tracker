from django.contrib import admin
from .models import Habit

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'action', 'time', 'duration', 'periodicity', 'is_public')
    list_filter = ('user', 'is_public', 'is_pleasant')
    search_fields = ('action', 'place', 'user__username')