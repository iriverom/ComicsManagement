from django.urls import path, include
from django.conf.urls import url
from django.views.generic import TemplateView
from . import views
from .views import remove_client, approve_group

urlpatterns = [
    path("", views.index, name="index"),
    # path("accounts/", include("django.contrib.auth.urls")),  # new
    path("index/", views.index, name="index"),
    path("excel/", views.some_view, name="excel"),
    path("search/", views.search_view, name="search_view"),
    path("graph/", views.dashboard_site, name="dashboard"),
    path("client/", views.client_index, name="client"),
    path("series/", views.series_index, name="series"),
    path("series/<slug:slug>/", views.series_subscription, name="series_subscription"),
    path("series/<slug:slug>", views.series_subscription, name="series_subscription"),
    path("client/<slug:slug>/", views.client_subscription, name="client_subscription"),
    path("client/<slug:slug>", views.client_subscription, name="client_subscription"),
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
    path(
        "delete/<pk>",
        remove_client.as_view(),
        name="remove_client",
    ),
    path(
        "change/<pk>/",
        views.approve_group,
        name="change_status",
    ),
]