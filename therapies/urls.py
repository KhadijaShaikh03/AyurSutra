from django.urls import path
from .views import therapy_list

urlpatterns = [
    path('', therapy_list),
]