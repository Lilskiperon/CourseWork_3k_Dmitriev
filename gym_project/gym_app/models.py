from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.db import models
from datetime import timedelta
from django.conf import settings

# Модель пользователя
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('trainer', 'Trainer'),
        ('participant', 'Participant'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='participant')
    photo = models.ImageField(upload_to='trainer_photos/', blank=True, null=True, verbose_name="Фото")
    bio = models.TextField(blank=True, null=True, verbose_name="Описание")

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return self.username

class Subscription(models.Model):
    DURATION_CHOICES = [
        (1, "1 месяц"),
        (3, "3 месяца"),
        (6, "6 месяцев"),
        (12, "12 месяцев"),
    ]
    DURATION_PRICES = {
        1: 500,   # Цена за 1 месяц
        3: 1400,  # Цена за 3 месяца
        6: 2700,  # Цена за 6 месяцев
        12: 5000, # Цена за 1 год
    }
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="subscriptions", verbose_name="Клиент")
    duration = models.PositiveIntegerField(choices=DURATION_CHOICES, verbose_name="Длительность")
    start_date = models.DateField(default=now, verbose_name="Дата начала")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    active = models.BooleanField(default=True, verbose_name="Активен")

    @property
    def end_date(self):
        return self.start_date + timedelta(days=self.duration * 30)
    def save(self, *args, **kwargs):
        # Устанавливаем цену на основе длительности
        if not self.price:
            self.price = self.DURATION_PRICES[self.duration]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.get_duration_display()}"

    class Meta:
        verbose_name = "Абонемент"
        verbose_name_plural = "Абонементы"

# Модель новостей
class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to='static/news_images/', blank=True, null=True, verbose_name="Фото")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")

    def __str__(self):
        return self.title
    
# Модель расписания тренировок
class TrainingSchedule(models.Model):
    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'trainer'},
        related_name='trainings_as_trainer',
        verbose_name="Тренер"
    )
    participant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'participant'},
        related_name='trainings_as_participant',
        verbose_name="Участник"
    )
    date = models.DateField(verbose_name="Дата")
    time = models.TimeField(verbose_name="Время")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Расписание тренировки"
        verbose_name_plural = "Расписание тренировок"
        unique_together = ('date', 'time', 'participant')
        
    def __str__(self):
        return f"{self.date} {self.time} - {self.trainer.username} с {self.participant.username}"
