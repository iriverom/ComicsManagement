from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("client/", views.client_index, name="client"),
    path("client/<slug:slug>/", views.client_suscription, name="suscription"),
    path("client/<slug:slug>", views.client_suscription, name="suscription"),
    path("test/", views.test_site, name="test"),
]