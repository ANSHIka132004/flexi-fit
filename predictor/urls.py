# File: predictor/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),

    path('', views.landing_view, name='landing'),
    path('analyzer/', views.daily_analyzer_view, name='analyzer'),
    path('analyzer/update/', views.update_health_data, name='update_health_data'),
    path('predict/', views.predict_view, name='predict'),
    path('meal_planner/', views.meal_planner_view, name='meal_planner'),
    path('workout_planner/', views.workout_planner_view, name='workout_planner'),
    path('voice_goal/', views.voice_goal_view, name='voice_goal'),
]
