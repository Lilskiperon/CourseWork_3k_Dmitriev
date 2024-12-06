from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import TrainingSchedule,News,CustomUser,Subscription
from django.utils.timezone import now

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'photo', 'bio']

class TrainingScheduleForm(forms.ModelForm):
    class Meta:
        model = TrainingSchedule
        fields = ['date', 'time', 'participant', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'min': now().date()}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
        labels = {
            'date': 'Дата тренировки',
            'time': 'Время тренировки',
            'participant': 'Клиент',
            'description': 'Описание',
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        time = cleaned_data.get("time")
        participant = cleaned_data.get("participant")

        if TrainingSchedule.objects.filter(date=date, time=time).exists():
            raise forms.ValidationError("На указанное время уже назначена тренировка.")

        return cleaned_data

class TrainerForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'bio', 'photo'] 
           
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите описание', 'rows': 5}),
        }
class SubscriptionPurchaseForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['duration']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['duration'].label = "Выберите длительность абонемента"