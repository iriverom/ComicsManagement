from django import forms
from django.forms import ModelForm
from app.models import Client, Subscription


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = [
            "client_number",
            "first_name",
            "last_name",
            "birthdate",
            "registration_date",
            "address",
            "email_address",
        ]
        widgets = {
            "client_number": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "birthdate": forms.DateInput(attrs={"class": "form-control"}),
            "registration_date": forms.DateInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "email_address": forms.EmailInput(attrs={"class": "form-control"}),
        }


class SubscriptionForm(ModelForm):
    class Meta:
        model = Subscription
        fields = [
            "client",
            "series",
            "begin_date",
            "end_date",
        ]

        # address = forms.CharField(blank=True)
        widgets = {
            "client": forms.TextInput(attrs={"class": "form-control"}),
            "series": forms.TextInput(attrs={"class": "form-control"}),
            "begin_date": forms.DateInput(attrs={"class": "form-control"}),
            "end_date": forms.DateInput(attrs={"class": "form-control"}),
        }
