from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from app.data_processing import get_df_marvel, visualize_comics
from app.models import Client, Comic, Series, Suscription
import pandas as pd


def index(request):
    df = visualize_comics()
    df = df.to_html()
    return HttpResponse(df)


def test_site(request):
    return render(request, "add_client_form.html", {})


def client_index(request):
    latest_client_list = Client.objects.order_by("-client_number")
    context = {"latest_client_list": latest_client_list}
    return render(request, "client_table.html", context)


def client_suscription(request, slug):
    slug_field = slug  # there's very likely a better way of doing this: https://learndjango.com/tutorials/django-slug-tutorial
    client_id = get_object_or_404(Client, client_number=slug).id
    suscription_list = Suscription.objects.filter(client=client_id)
    context = {"slug_field": slug_field, "suscription_list": suscription_list}
    return render(request, "suscription_table.html", context)
