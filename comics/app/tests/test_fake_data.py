from app.fake_data import create_fake_clients, create_fake_subscriptions
from app.models import Client, Subscription
import pytest

pytestmark = pytest.mark.django_db


def test_create_fake_clients():
    assert not Client.objects.all()
    create_fake_clients()
    assert Client.objects.all().count() == 99


def test_create_fake_subscriptions():
    Client.objects.create(
        client_number=548,
        first_name="Ivan",
        last_name="Rivero",
        birthdate="1986-08-05",
        registration_date="2021-03-23",
        email_address="test@gmail.com",
    )
    assert Client.objects.all().count() == 1
    assert not Subscription.objects.all()


#    create_fake_subscriptions()
#    assert Subscription.objects.all()
