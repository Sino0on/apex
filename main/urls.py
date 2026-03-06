from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('course_detail/', course_detail, name='course_detail'),
    path('category_detail/', category_detail, name='category_detail'),
    path('univer/<int:pk>', univer, name='univer'),
    path('business-service/<int:pk>/', business_service_detail, name='business_service_detail'),
    path('zoom-register/', zoom_register, name='zoom_register'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
]
