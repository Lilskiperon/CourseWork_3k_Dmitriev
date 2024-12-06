from django.utils.timezone import now, timedelta
from django.core.mail import send_mail
from .models import TrainingSchedule

def send_training_notifications():
    upcoming_date = now().date() + timedelta(days=1)
    trainings = TrainingSchedule.objects.filter(date=upcoming_date)
    for training in trainings:
        for participant in training.participants.all():
            send_mail(
                subject='Напоминание о тренировке',
                message=f'Здравствуйте, {participant.username}! Завтра у вас тренировка с {training.trainer.username} в {training.time}.',
                from_email='no-reply@gymapp.com',
                recipient_list=[participant.email],
            )
