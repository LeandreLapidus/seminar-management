"""
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('dashboard/', admin.site.urls),
    path('course/', include('course.urls')),
    path('', include('account.urls'))
]
