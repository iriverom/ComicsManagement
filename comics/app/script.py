import pandas as pd
from app.models import Client, Series, Comic, Subscription
from faker import Faker
from datetime import date
from app.data_processing import get_df_from_txt, adding_comics
from app.fake_data import create_fake_clients, create_fake_subscriptions


def populate_database():
    create_fake_clients()
    adding_comics()
    create_fake_subscriptions()