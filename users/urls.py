from django.urls import path

import users.views as views

urlpatterns = [
  path('permissions/', views.permissions, name='permissions'),
  path('auth/', views.authenticate, name='auth'),
  path('cas/', views.cas_validation, name='cas'),
]
