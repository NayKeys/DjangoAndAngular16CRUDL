from django.urls import path

import datahub.views as views

urlpatterns = [
  path('execute/', views.execute, name='execute'),
]