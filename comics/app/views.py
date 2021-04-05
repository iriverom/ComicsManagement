from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from app.data_processing import get_df_marvel, visualize_comics
from app.models import Client, Comic, Series, Suscription
import pandas as pd
from app.addclientform import NameForm, ClientForm
from django.urls import reverse


def index(request):
    df = visualize_comics()
    df = df.to_html()
    return HttpResponse(df)


def add_client(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = ClientForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            print(request.POST)
            f = form.save()
            return HttpResponseRedirect(reverse("client"))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ClientForm()

    return render(request, "add-client-form.html", {"form": form})


def client_index(request):
    latest_client_list = Client.objects.order_by("-client_number")
    context = {"latest_client_list": latest_client_list}
    return render(request, "client_table.html", context)


def client_subscription(request, slug):
    slug_field = slug  # there's very likely a better way of doing this: https://learndjango.com/tutorials/django-slug-tutorial
    client_id = get_object_or_404(Client, client_number=slug).id
    subscription_list = Suscription.objects.filter(client=client_id)
    context = {"slug_field": slug_field, "subscription_list": subscription_list}
    return render(request, "subscription_table.html", context)
