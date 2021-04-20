from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from app.data_processing import get_df_marvel, visualize_comics
from app.models import Client, Comic, Series, Suscription
from app.graph_data import count_data, client_subscription_classification
import pandas as pd
from django import forms
from app.addforms import ClientForm, SubscriptionForm
from django.urls import reverse
import datetime


def graphsite(request):
    x = count_data(Series, "series")
    y = client_subscription_classification()
    context = {**x, **y}
    return render(request, "graph_test.html", context)


def index(request):
    df = visualize_comics()
    df = df.to_html()
    return HttpResponse(df)


def add_client(request):
    if request.method == "POST":
        form = ClientForm(
            request.POST
        )  # Here maybe look into "instances" https://docs.djangoproject.com/en/3.1/topics/forms/modelforms/#the-save-method
        if form.is_valid():
            form.save()
            print(request.POST)
            return HttpResponseRedirect(reverse("client"))
    else:
        form = ClientForm()
    return render(request, "add-client-form.html", {"form": form})


def add_subscription(request, slug):
    if request.method == "POST":
        form_data = request.POST.copy()
        form_data["client"] = Client.objects.get(client_number=slug).id
        print(form_data)
        form = SubscriptionForm(
            form_data
        )  # Here maybe look into "instances" https://docs.djangoproject.com/en/3.1/topics/forms/modelforms/#the-save-method
        if form.is_valid():
            form.save()
            print(request.POST)

            return HttpResponseRedirect(reverse("client"))
    else:

        SubscriptionForm.base_fields["client"] = forms.ModelChoiceField(
            Client.objects.filter(client_number=slug),
            widget=forms.Select(attrs={"class": "form-control"}),
            disabled=False,  # Try to make it true!!!!!!!!!!
        )
        SubscriptionForm.base_fields["series"] = forms.ModelChoiceField(
            Series.objects.all(), widget=forms.Select(attrs={"class": "form-control"})
        )
        form = SubscriptionForm(
            initial={
                "client": Client.objects.get(client_number=slug),
                "begin_date": datetime.datetime.now(),
            }
        )

    url_test = "/app/client/<slug:slug>/suscriptionadded"
    return render(
        request,
        "add-subscription-form.html",
        {"form": form, "slug": slug, "url_test": url_test},
    )


def client_index(request):
    latest_client_list = Client.objects.order_by("-client_number")
    context = {"latest_client_list": latest_client_list}
    return render(request, "client_table.html", context)


def client_subscription(request, slug):
    slug_field = slug  # there's very likely a better way of doing this: https://learndjango.com/tutorials/django-slug-tutorial
    client_id = get_object_or_404(Client, client_number=slug).id
    subscription_list = Suscription.objects.filter(client=client_id)
    context = {
        "slug_field": slug_field,
        "subscription_list": subscription_list,
        "client_id": client_id,
    }
    return render(request, "subscription_table.html", context)
