"""
URL configuration for HMA_Calendar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('HMA_Calendar/admin/', admin.site.urls),
    # path('HMA_Calendar/',include('calendar_app.urls')),
    path('cal2026/admin/', admin.site.urls),
    path('cal2026/', include('calendar_app.urls')),
    path('adminpanel/', include('adminapp.urls')),
    path('', include('pwa.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
