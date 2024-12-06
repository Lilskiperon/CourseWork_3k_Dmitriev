from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('news/', views.news_list, name='news_list'),
    path('news/add/', views.add_news, name='add_news'),
    path('news/edit/<int:pk>/', views.edit_news, name='edit_news'),
    path('news/delete/<int:pk>/', views.delete_news, name='delete_news'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('news/add/', views.add_news, name='add_news'),
    path('schedules/all', views.view_all_schedules, name='admin_schedules'),
    path('trainers/', views.trainer_list, name='trainer_list'),
    path('trainer/<int:trainer_id>/', views.trainer_details, name='trainer_details'),
    path('trainers/edit/<int:pk>/', views.edit_trainer, name='edit_trainer'),
    path('trainers/delete/<int:pk>/', views.delete_trainer, name='delete_trainer'),
    path('users/', views.users_list, name='users_list'),
    path('training/', views.schedule, name='trainings_list'),
    path('training/add/', views.add_training, name='add_training'),
    path('assign-trainer/<int:user_id>/', views.assign_trainer, name='assign_trainer'),
    path('subscriptions/', views.subscriptions_list, name='subscriptions_list'),
    path('subscriptions/purchase/', views.purchase_subscription, name='purchase_subscription'),
    path('subscriptions/available/', views.available_subscriptions, name='available_subscriptions'),
]

