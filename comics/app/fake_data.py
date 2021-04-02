from faker import Faker
import pandas as pd
from app.models import Client, Series, Comic, Suscription

fake = Faker("de_DE")
# data = []


def create_fake_clients():
    for i in range(49):
        c = Client.objects.get_or_create(
            client_number=fake.pyint(min_value=100, max_value=999),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            birthdate=fake.date_of_birth(minimum_age=18, maximum_age=75).strftime(
                "%Y-%m-%d"
            ),
            registration_date=fake.date_time_this_decade().strftime("%Y-%m-%d"),
            address=fake.street_address() + fake.city_with_postcode(),
            email_address=fake.ascii_safe_email(),
        )
