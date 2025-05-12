# predictor/urls.py
from django.urls import path
from . import views

app_name = 'predictor'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('predict/job/', views.predict_job_view, name='predict_job'),
    path('predict/degree/', views.predict_degree_view, name='predict_degree'),
    path('history/', views.prediction_history, name='history'),
    path('profile/', views.profile_view, name='profile'),
]