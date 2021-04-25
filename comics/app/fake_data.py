from faker import Faker
from app.models import Client, Series, Comic, Subscription
from datetime import date
import random

fake = Faker("de_DE")


def create_fake_clients():
    for i in range(1, 100):
        c = Client.objects.get_or_create(
            client_number=i,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            birthdate=fake.date_of_birth(minimum_age=18, maximum_age=75).strftime(
                "%Y-%m-%d"
            ),
            registration_date=fake.date_time_this_decade().strftime("%Y-%m-%d"),
            address=fake.street_address() + fake.city_with_postcode(),
            email_address=fake.ascii_safe_email(),
        )


def create_fake_subscriptions():
    for client in Client.objects.all():
        for i in range(fake.pyint(min_value=0, max_value=12)):
            begin_date = fake.date_time_between_dates(
                client.registration_date, date.today()
            )
            end_date = fake.date_time_between_dates(begin_date, date.today()).strftime(
                "%Y-%m-%d"
            )
            if random.choices([True, False], weights=[1, 10]):
                end_date = None
            begin_date = begin_date.strftime("%Y-%m-%d")
            s = Subscription.objects.get_or_create(
                client=client,
                series=Series.objects.get(
                    pk=fake.pyint(min_value=1, max_value=Series.objects.all().count())
                ),
                begin_date=begin_date,
                end_date=end_date,
            )
            # create a way to not have end_date
