from django.urls import path

import datahub.views as views

urlpatterns = [
  path('execute/', views.execute, name='execute'),
  path('viewtree/', views.view_tree, name='view_tree'),
]