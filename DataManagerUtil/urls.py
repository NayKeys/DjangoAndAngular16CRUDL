from django.urls import path

from . import views

urlpatterns = [
  path('execute/', views.execute, name='execute'),
]
