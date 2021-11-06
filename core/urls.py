from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core import views

urlpatterns = [
    path("clients/create", views.RegisterView.as_view()),
    path("clients/login", views.LoginView.as_view()),
    path("clients/<int:pk>/match", views.EstimationView.as_view()),
    path("list", views.UserListView.as_view()),
]
