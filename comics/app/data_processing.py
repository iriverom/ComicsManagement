import pandas as pd
from app.models import Client, Series, Comic, Subscription
from django.db.models import Count, Q
from datetime import date
import urllib.request


def process_previews_file():
    """
    Downloads the comics previews file and parses it.
    """
    url = "https://www.previewsworld.com/Catalog/CustomerOrderForm/TXT/JAN21"
    f = urllib.request.urlopen(url)
    lines = f.read().decode("windows-1252").splitlines()

    comic_list = []
    for line in lines:
        if not (line[0:4] == "PAGE" or line.count("#") > 1):
            if line[-2:-1] == "$":
                comic_split = line.split("\t")
                comic_split.append(publisher)
                comic_list.append(comic_split)
            else:
                publisher = line.split("\t")[0]

    cols = [
        "Weird",
        "Code",
        "Name",
        "Release Date",
        "Price",
        "Currency",
        "Empty",
        "Publisher",
    ]
    df = pd.DataFrame(comic_list, columns=cols)

    df = df[df["Code"].notnull()]
    df[["Name", "Description"]] = df["Name"].str.split(
        "#",
        expand=True,
    )
    df["Issue"] = df["Description"].str.split(" ").str[0]
    df["Price"] = df["Price"].str.split("$").str[1]
    df = df.drop(["Weird", "Currency", "Empty"], 1)

    df["Description"] = df["Description"].str.split(" ").str[1:]
    df["Name"] = df["Name"].str.strip()
    df["Release Date"] = pd.to_datetime(df["Release Date"]).dt.date
    return df


def adding_comics():
    """
    Adds all the new monthly comics to the database
    """
    df = process_previews_file()
    df = df[df["Price"].notnull()]
    df = df[df["Issue"].notnull()]
    for i in range(len(df.index)):
        # this way all TPBs and HC are thrown out, a more elegant way should be implemented
        issue_number = df["Issue"].iloc[i]
        comic_name = df["Name"].iloc[i]
        # comic_name_underscore = df["Name2"].iloc[i]
        price = df["Price"].iloc[i]
        publisher = df["Publisher"].iloc[i].capitalize()
        release_date = df["Release Date"].iloc[i]
        s, created = Series.objects.get_or_create(
            publisher=publisher,
            name=comic_name,
            volume=1,
        )
        c = Comic.objects.get_or_create(
            series=s, issue=issue_number, pub_date=release_date, price=price
        )


# importing of HC and TPB not implemented


def create_excel_order_monthly():
    data_count = Series.objects.annotate(
        num_subs=Count("subscription", filter=Q(subscription__end_date__isnull=True))
    )
    comic_data = []
    for series in data_count:
        if series.num_subs != 0:
            comicqueryset = Comic.objects.filter(
                series=series.id, pub_date__month=date.today().month - 2
            )  # month - 2 is for testing purposes, once the database is properly filled and only give the order form for the actual month
            for comic in comicqueryset:
                issue_data = [
                    series.publisher,
                    series.name,
                    comic.issue,
                    comic.pub_date.strftime("%Y-%m-%d"),
                    comic.price,
                    series.num_subs,
                    comic.price * series.num_subs,
                ]
                comic_data.append(issue_data)
    cols = [
        "Publisher",
        "Series Name",
        "Issue",
        "Release Date",
        "Price",
        "Amount",
        "Total price",
    ]
    df = pd.DataFrame(comic_data, columns=cols)
    return df
