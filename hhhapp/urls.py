from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('logout', views.logout),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('hikes/new', views.new),
    path('hikes/new/create', views.create),
    path('hikes/<int:hike_id>/hikedetails', views.viewhike),
    path('hikes/<int:hike_id>/delete', views.delete),
    path('hikes/<int:hike_id>/edit', views.edit),
    path('hikes/<int:hike_id>/update', views.update),
    path('join/<int:hike_id>', views.join),
    path('unjoin/<int:hike_id>', views.notjoin),
]