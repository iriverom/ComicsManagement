from app.models import Client, Subscription, Series, Comic
from app.graph_data import count_data, _client_subscription_classification
import pytest

pytestmark = pytest.mark.django_db


def test_count_data():
    sbat = Series.objects.create(publisher="DC", name="Batman", volume=1)
    ssup = Series.objects.create(publisher="DC", name="Superman", volume=1)
    c = Client.objects.create(
        client_number=548,
        first_name="Ivan",
        last_name="Rivero",
        birthdate="1986-08-05",
        registration_date="2021-03-23",
        email_address="test@gmail.com",
    )
    cl = Client.objects.create(
        client_number=1,
        first_name="Test",
        last_name="Tester",
        birthdate="1990-08-05",
        registration_date="2021-01-23",
        email_address="test@gmail.com",
    )

    Subscription.objects.create(series=sbat, client=cl, begin_date="2021-01-03")
    Subscription.objects.create(series=sbat, client=c, begin_date="2021-01-03")
    Subscription.objects.create(series=ssup, client=cl, begin_date="2021-01-03")
    context = count_data(Series, "series", 10)
    assert context["labels_series_counts"] == ["Superman Volume 1", "Batman Volume 1"]
    assert context["data_series_counts"] == [1, 2]


def test_client_subscription_classification():
    sbat = Series.objects.create(publisher="DC", name="Batman", volume=1)
    ssup = Series.objects.create(publisher="DC", name="Superman", volume=1)
    c = Client.objects.create(
        client_number=548,
        first_name="Ivan",
        last_name="Rivero",
        birthdate="1986-08-05",
        registration_date="2021-03-23",
        email_address="test@gmail.com",
    )
    cl = Client.objects.create(
        client_number=1,
        first_name="Test",
        last_name="Tester",
        birthdate="1990-08-05",
        registration_date="2021-01-23",
        email_address="test@gmail.com",
    )

    Subscription.objects.create(series=sbat, client=cl, begin_date="2021-01-03")
    Subscription.objects.create(series=sbat, client=c, begin_date="2021-01-03")
    Subscription.objects.create(series=ssup, client=cl, begin_date="2021-01-03")
    context = _client_subscription_classification()
    assert context["labels_client_counts"] == [
        "Customers with 1 subscriptions",
        "Customers with 2 subscriptions",
    ]
    assert context["data_client_counts"] == [1, 1]
