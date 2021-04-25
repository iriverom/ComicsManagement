from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from app.data_processing import (
    get_df_marvel,
    visualize_comics,
    create_excel_order_monthly,
)
from app.models import Client, Comic, Series, Subscription
from app.graph_data import count_data, _client_subscription_classification
import pandas as pd
from django import forms
from app.addforms import ClientForm, SubscriptionForm
from django.urls import reverse
from django.db.models import Q
import datetime
from datetime import date
from io import BytesIO


def dashboard_site(request):
    x = count_data(Series, "series", 9)
    y = _client_subscription_classification()
    context = {**x, **y}
    return render(request, "dashboard.html", context)


def some_view(request):
    df = create_excel_order_monthly()
    with BytesIO() as b:
        writer = pd.ExcelWriter(b, engine="xlsxwriter")
        excelname = (
            "Order_Form_"
            + date.today().strftime("%m")
            + "_"
            + str(date.today().year)
            + ".xlsx"
        )
        df.to_excel(writer, sheet_name=excelname, index=False)
        writer.save()
        filename = excelname + ".xlsx"
        response = HttpResponse(
            b.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = "attachment; filename=%s" % filename
        return response


def index(request):
    # df = visualize_comics()
    # df = df.to_html()
    # return HttpResponse(df)
    return render(request, "index.html")


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

    url_test = "/app/client/<slug:slug>/subscriptionadded"
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
    subscription_list = Subscription.objects.filter(client=client_id)
    context = {
        "slug_field": slug_field,
        "subscription_list": subscription_list,
        "client_id": client_id,
    }
    return render(request, "subscription_table.html", context)


def series_index(request):
    series_list = Series.objects.order_by("publisher")
    context = {"series_list": series_list}
    return render(request, "series_table.html", context)


def search_view(request):

    search_req = request.GET.get("search")
    if search_req:
        series_list = Series.objects.filter(Q(name__icontains=search_req))
        client_list = Client.objects.filter(Q(client_number__icontains=search_req))
    if series_list:
        context = {"series_list": series_list}
        template = "series_table.html"
    elif client_list:
        context = {"latest_client_list": client_list}
        template = "client_table.html"
    else:
        template = "404.html"
        context = {}
    return render(request, template, context)


def series_subscription(request, slug):
    slug_field = slug  # there's very likely a better way of doing this: https://learndjango.com/tutorials/django-slug-tutorial
    series_id = get_object_or_404(Series, id=slug).id
    series_name = get_object_or_404(Series, id=slug).name
    subscription_list = Subscription.objects.filter(series=series_id)
    context = {
        "slug_field": slug_field,
        "subscription_list": subscription_list,
        "series_id": series_id,
        "series_name": series_name,
    }
    return render(request, "series_subscription_table.html", context)
