from django.contrib import admin
from django.utils.html import format_html
from .models import News, CustomUser, TrainingSchedule,Subscription

# Регистрация модели News
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'image_preview')
    list_filter = ('created_at',)
    search_fields = ('title', 'content')
    ordering = ('-created_at',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 75px; height: auto;">', obj.image.url)
        return "Нет изображения"
    image_preview.short_description = "Превью изображения"

# Регистрация модели CustomUser
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff')
    search_fields = ('username', 'email')

# Регистрация модели TrainingSchedule
@admin.register(TrainingSchedule)
class TrainingScheduleAdmin(admin.ModelAdmin):
    list_display = ('trainer', 'date', 'time', 'participant')
    list_filter = ('date', 'trainer')
    search_fields = ('description',)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "duration", "start_date", "end_date", "active")
    list_filter = ("active", "duration")
    search_fields = ("user__username", "user__email")