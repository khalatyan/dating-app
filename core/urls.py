from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core import views

urlpatterns = [
    path("create", views.RegisterView.as_view()),
    path("login", views.LoginView.as_view()),
    # path("<int:pk>", views.EstimationDetailView.as_view()),
    path("<int:pk>/match", views.EstimationView.as_view()),
]
