from django.urls import path

import API.views as views

urlpatterns = [
  path('execute/', views.execute, name='execute'),
  path('csrf/', views.csrfToken, name='csrf'),
  path('auth/', views.casValidation, name='auth'),
  path('cas/', views.authenticate, name='cas')
]
