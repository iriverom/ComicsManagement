from app.models import Client, Subscription, Series, Comic
import pytest

pytestmark = pytest.mark.django_db


def test_client_model():
    cl = Client.objects.create(
        client_number=548,
        first_name="Ivan",
        last_name="Rivero",
        birthdate="1986-08-05",
        registration_date="2021-03-23",
        email_address="test@gmail.com",
    )
    assert Client.objects.all()
    assert str(cl) == "548 Ivan Rivero"


def test_series_model():
    s = Series.objects.create(publisher="DC", name="Batman", volume=3)
    assert str(s) == "Batman Volume 3"
    assert Series.objects.all()


def test_comic_model():
    s = Series.objects.create(publisher="DC", name="Batman", volume=3)
    c = Comic.objects.create(series=s, issue=90, pub_date="2021-03-01", price="3.99")
    assert str(c) == "Batman Volume 3 90"


def test_subscription_model():
    cl = Client.objects.create(
        client_number=548,
        first_name="Ivan",
        last_name="Rivero",
        birthdate="1986-08-05",
        registration_date="2021-03-23",
        email_address="test@gmail.com",
    )
    s = Series.objects.create(publisher="DC", name="Batman", volume=3)
    sus = Subscription.objects.create(series=s, client=cl, begin_date="2021-01-03")
    assert str(sus) == "548 Ivan Rivero Batman Volume 3"
