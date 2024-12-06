from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import News, TrainingSchedule,CustomUser,Subscription
from .forms import NewsForm,CustomUserCreationForm,TrainingScheduleForm,TrainerForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
# Главная страница
def home(request):
    news = News.objects.all().order_by('-created_at')[:5]
    return render(request, 'gym_app/home.html', {'news': news})

# Регистрация
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')  # Перенаправление на страницу входа
    else:
        form = CustomUserCreationForm()
    return render(request, 'gym_app/register.html', {'form': form})

# Вход
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'gym_app/login.html', {'form': form})

# Выход
def logout_view(request):
    logout(request)
    return redirect('home')

# Новости
def news_list(request):
    news_list = News.objects.all().order_by('-created_at')
    return render(request, 'gym_app/news_list.html', {'news_list': news_list})

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    return render(request, 'gym_app/news_detail.html', {'news': news})

# Расписание
def schedule(request):
    if not request.user.is_authenticated:
        # Для неавторизованных пользователей показать сообщение
        return render(request, 'gym_app/schedule.html', {'require_login': True})

    # Для авторизованных пользователей
    if request.user.role == 'participant':
        trainings = TrainingSchedule.objects.filter(participant=request.user)
    elif request.user.role == 'trainer':
        trainings = TrainingSchedule.objects.filter(trainer=request.user)
    elif request.user.role == 'admin':
        trainings = TrainingSchedule.objects.all()
    else:
        trainings = []  # Если роль не определена, показать пустое расписание

    return render(request, 'gym_app/schedule.html', {'trainings': trainings})

def add_training(request):
    if request.method == 'POST':
        form = TrainingScheduleForm(request.POST)
        if form.is_valid():
            training = form.save(commit=False)
            training.trainer = request.user  # Назначаем текущего пользователя как тренера
            training.save()
            messages.success(request, "Тренировка успешно добавлена!")
            return redirect('trainings_list')  # Перенаправляем на список тренировок
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = TrainingScheduleForm()

    return render(request, 'gym_app/add_training.html', {'form': form})

@login_required
# Список тренеров
def trainer_list(request):
    trainers = CustomUser.objects.filter(role='trainer')
    return render(request, 'gym_app/trainer_list.html', {'trainers': trainers})

# Редактирование тренера
@user_passes_test(lambda u: u.is_superuser)
def edit_trainer(request, pk):
    trainer = get_object_or_404(CustomUser, pk=pk, role='trainer')
    if request.method == 'POST':
        form = TrainerForm(request.POST, request.FILES, instance=trainer)
        if form.is_valid():
            form.save()
            return redirect('trainer_list')
    else:
        form = TrainerForm(instance=trainer)
    return render(request, 'gym_app/edit_trainer.html', {'form': form, 'trainer': trainer})

# Удаление тренера (сброс роли)
@user_passes_test(lambda u: u.is_superuser)
def delete_trainer(request, pk):
    trainer = get_object_or_404(CustomUser, pk=pk, role='trainer')
    if request.method == 'POST':
        trainer.role = 'participant'  # Сбрасываем роль на участника
        trainer.save()
        return redirect('trainer_list')
    return render(request, 'gym_app/delete_trainer.html', {'trainer': trainer})

# Добавление новости
@user_passes_test(lambda u: u.is_superuser)
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('news_list')
    else:
        form = NewsForm()
    return render(request, 'gym_app/add_news.html', {'form': form})

# Редактирование новости
@user_passes_test(lambda u: u.is_superuser)
def edit_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return redirect('news_list')
    else:
        form = NewsForm(instance=news)
    return render(request, 'gym_app/edit_news.html', {'form': form, 'news': news})

# Удаление новости
@user_passes_test(lambda u: u.is_superuser)
def delete_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        news.delete()
        return redirect('news_list')
    return render(request, 'gym_app/delete_news.html', {'news': news})

@login_required
def view_all_schedules(request):
    if request.user.role != 'admin':
        return render(request, 'gym_app/permission_denied.html')
    schedules = TrainingSchedule.objects.all()
    return render(request, 'gym_app/admin_schedules.html', {'schedules': schedules})

@login_required
def trainer_details(request, trainer_id):
    if request.user.role != 'admin':  # Проверяем, что пользователь — администратор
        return render(request, 'gym_app/permission_denied.html')
    
    try:
        trainer = CustomUser.objects.get(id=trainer_id, role='trainer')
    except CustomUser.DoesNotExist:
        return render(request, 'gym_app/not_found.html', status=404)
    
    return render(request, 'gym_app/trainer_details.html', {'trainer': trainer})

@login_required
def trainer_list(request):
    if request.user.role != 'admin':  # Проверяем, что пользователь — администратор
        return render(request, 'gym_app/permission_denied.html')
    
    trainers = CustomUser.objects.filter(role='trainer')
    return render(request, 'gym_app/trainer_list.html', {'trainers': trainers})

@login_required
def users_list(request):
    if request.user.role != 'admin':  # Только для администраторов
        return render(request, 'gym_app/permission_denied.html')
    users = CustomUser.objects.exclude(id=request.user.id)  # Исключаем текущего администратора
    return render(request, 'gym_app/users_list.html', {'users': users})

@login_required
def assign_trainer(request, user_id):
    if request.user.role != 'admin':  # Только для администраторов
        return render(request, 'gym_app/permission_denied.html')
    user = get_object_or_404(CustomUser, id=user_id)
    user.role = 'trainer'
    user.save()
    return redirect('users_list')

@login_required
def subscriptions_list(request):
    if request.user.role == "admin":
        subscriptions = Subscription.objects.all()
    else:
        subscriptions = Subscription.objects.filter(user=request.user)

    return render(request, "gym_app/subscriptions_list.html", {"subscriptions": subscriptions})

@login_required
def purchase_subscription(request):
    if request.method == "POST":
        # Проверяем, есть ли у пользователя активный абонемент
        active_subscription = Subscription.objects.filter(user=request.user, active=True).first()
        if active_subscription:
            messages.error(request, "У вас уже есть активный абонемент!")
            return redirect('available_subscriptions')

        # Получаем длительность из POST-запроса
        duration = int(request.POST.get("duration"))
        price = Subscription.DURATION_PRICES[duration]

        # Создаём новый абонемент
        Subscription.objects.create(
            user=request.user,
            duration=duration,
            price=price,
            active=True
        )
        messages.success(request, "Абонемент успешно приобретён!")
        return redirect('subscriptions_list')  # Перенаправление на список абонементов
    return redirect('available_subscriptions')
@login_required
def available_subscriptions(request):
    # Доступные варианты абонементов
    available_options = [
        {"duration": 1, "price": Subscription.DURATION_PRICES[1], "description": "1 месяц"},
        {"duration": 3, "price": Subscription.DURATION_PRICES[3], "description": "3 месяца"},
        {"duration": 6, "price": Subscription.DURATION_PRICES[6], "description": "6 месяцев"},
        {"duration": 12, "price": Subscription.DURATION_PRICES[12], "description": "1 год"},
    ]

    return render(request, 'gym_app/available_subscriptions.html', {"available_options": available_options})