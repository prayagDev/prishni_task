
from django.contrib import admin
from django.urls import path
from app1.views import dataview, generate_certificate, verify_certificate

urlpatterns = [
    path('data/', dataview, name="dataview"),
    path('generate-certificate/<int:teacher_id>/', generate_certificate, name='generate_certificate'),
    path('verify-certificate/<str:token>/', verify_certificate, name='verify_certificate'),
    path('admin/', admin.site.urls),
]
