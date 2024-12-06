from django.core.management.base import BaseCommand
from gym_app.tasks import send_training_notifications

class Command(BaseCommand):
    help = 'Send training notifications to participants'

    def handle(self, *args, **kwargs):
        send_training_notifications()
        self.stdout.write('Уведомления отправлены!')
