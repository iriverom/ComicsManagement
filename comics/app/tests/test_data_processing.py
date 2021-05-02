from app.models import Client, Subscription, Series, Comic
from app.data_processing import (
    process_previews_file,
    adding_comics,
    create_excel_order_monthly,
)
import datetime
import pytest


pytestmark = pytest.mark.django_db


def test_process_previews_file():
    # url = "https://www.previewsworld.com/Catalog/CustomerOrderForm/TXT/JAN21"
    df = process_previews_file()
    assert df["Code"][0] == "JAN21 0001"
    assert df["Name"][0] == "PREVIEWS"
    rel_date = datetime.datetime.strptime("2021-02-24", "%Y-%m-%d").date()
    assert df["Release Date"][0] == rel_date
    assert df["Price"][0] == "3.99"
    assert df["Publisher"][0] == "PREVIEWS PUBLICATIONS"
    assert df["Issue"][0] == "390"


def test_adding_comics():
    adding_comics()
    assert Series.objects.get(name="PREVIEWS")
    series_id = Series.objects.get(name="PREVIEWS").id
    assert Comic.objects.get(series=series_id)


def test_create_excel_order_monthly():
    s = Series.objects.create(publisher="DC", name="Batman", volume=3)
    co = Comic.objects.create(series=s, issue=90, pub_date="2021-03-01", price="3.99")
    co = Comic.objects.create(series=s, issue=91, pub_date="2021-03-22", price="3.99")
    cl = Client.objects.create(
        client_number=548,
        first_name="Ivan",
        last_name="Rivero",
        birthdate="1986-08-05",
        registration_date="2021-03-23",
        email_address="test@gmail.com",
    )
    Subscription.objects.create(series=s, client=cl, begin_date="2021-01-03")
    assert Series.objects.all()
    assert Comic.objects.all()
    assert Client.objects.all()
    assert Subscription.objects.all()
    df = create_excel_order_monthly()
    assert df["Publisher"][0] == "DC"
    assert df["Series Name"][0] == "Batman"
    assert df["Issue"][0] == 90
    assert df["Release Date"][0] == "2021-03-01"
    assert df["Price"][0] == 3.99
    assert df["Amount"][0] == 1
    assert df["Total price"][0] == 3.99
    assert df["Issue"][1] == 91