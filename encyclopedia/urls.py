from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('<str:name>', views.entries, name='read_entrys'),
    path("createnewpage/", views.createnewpage, name="createnewpage"),
    path('randompage/', views.randompage, name="randompage")
]
