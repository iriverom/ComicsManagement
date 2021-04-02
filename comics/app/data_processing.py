import pandas as pd
from app.models import Client, Series, Comic, Suscription


def get_df_marvel():
    my_cols = ["Page", "Code", "Name", "Release Date", "Price", "Currency"]
    df = pd.read_csv(r"/mnt/d/DataAnalysis/Marvel_January_21.csv", names=my_cols)

    df = df[df["Code"].notnull()]  # filtering all not null lines

    df[["Name", "Description"]] = df["Name"].str.split(
        "#",
        expand=True,
    )
    df["Number"] = df["Description"].str.split(" ").str[0]
    df["Price"] = df["Price"].str.split("$").str[1]
    df["Description"] = df["Description"].str.split(" ").str[1:]
    df["Release Date"] = pd.to_datetime(df["Release Date"])
    df = df.drop(["Page", "Currency"], 1)
    return df


# from app.data_processing import adding_comics


def adding_comics():
    df = get_df_marvel()
    for i in range(len(df.index)):
        issue_number = df["Number"].iloc[i]
        comic_name = df["Name"].iloc[i]
        publisher = "Marvel"
        release_date = df["Release Date"].iloc[i]
        s, created = Series.objects.get_or_create(
            publisher=publisher, name=comic_name, volume=1
        )
        c = Comic.objects.get_or_create(
            series=s, issue=issue_number, pub_date=release_date
        )


# handling of HC and TPB not implemented


def visualize_comics():
    df = pd.DataFrame(list(Comic.objects.all().values()))
    series_id_column = df["series_id"]
    new_id_column = []
    for i in range(len(series_id_column)):
        new_id_column.append(Series.objects.get(pk=series_id_column[i]).name)
    df = df.drop("series_id", axis=1)  # inplace = True
    df["series_name"] = pd.Series(new_id_column).values
    return df
