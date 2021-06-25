from app.data_processing import adding_comics
from app.fake_data import create_fake_clients, create_fake_subscriptions


def populate_database():
    create_fake_clients()
    print("Fake Clients created")
    adding_comics()
    print("Comics added")
    create_fake_subscriptions()
    print("Fake Subscriptions created")