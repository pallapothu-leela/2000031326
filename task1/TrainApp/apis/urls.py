from django.urls import path
from . import views

urlpatterns = [
    path('trains/', views.get_train_schedule),
    path('train/<pk>', views.get_train)
]