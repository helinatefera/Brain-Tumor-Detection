from django.urls import path
from . import views
urlpatterns=[
    path('front/',views.front,name='front'),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('api/', views.brain_api, name='api')
]
