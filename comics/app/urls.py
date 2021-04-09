from django.urls import path
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("client/", views.client_index, name="client"),
    path("client/<slug:slug>/", views.client_subscription, name="subscription"),
    path("client/<slug:slug>", views.client_subscription, name="subscription"),
    path("addclient/", views.add_client, name="addclient"),
    path("clientadded/", views.add_client, name="clientadded"),
    path(
        "client/<slug:slug>/addsubscription",
        views.add_subscription,
        name="addsubscription",
    ),
    path(
        "client/<slug:slug>/subscriptionadded/",
        views.add_subscription,
        name="subscriptionadded",
    ),
]