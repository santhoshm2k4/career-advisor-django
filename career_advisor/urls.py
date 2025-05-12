"""
URL configuration for career_advisor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# career_advisor/career_advisor/urls.py
from django.contrib import admin
from django.urls import path, include
from predictor import views as predictor_views # Import predictor views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('predictor.urls')), # Keep your app URLs
    path('accounts/', include('django.contrib.auth.urls')), # Keep auth URLs

    # Add the registration URL
    path('accounts/register/', predictor_views.register, name='register'),
]
