from django.urls import path

import API.views as views

urlpatterns = [
  path('execute/', views.execute, name='execute'),
  path('auth/', views.authenticate, name='auth'),
  path('cas/', views.cas_validation, name='cas')
]
