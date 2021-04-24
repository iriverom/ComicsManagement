import pandas as pd
from app.models import Client, Series, Comic, Subscription


def get_df_from_txt():
    with open(
        r"/mnt/d/DataAnalysis/JAN21_COF.txt", "r", encoding="unicode_escape"
    ) as f:
        mylist = f.read().splitlines()

    comic_list = []
    for element in mylist:
        if not (element[0:4] == "PAGE" or element.count("#") > 1):
            if element[-2:-1] == "$":
                comic_split = element.split("\t")
                comic_split.append(publisher)
                comic_list.append(comic_split)
            else:
                publisher = element.split("\t")[0]

    my_cols = [
        "Weird",
        "Code",
        "Name",
        "Release Date",
        "Price",
        "Currency",
        "Empty",
        "Publisher",
    ]
    df = pd.DataFrame(comic_list, columns=my_cols)

    df = df[df["Code"].notnull()]
    df[["Name", "Description"]] = df["Name"].str.split(
        "#",
        expand=True,
    )
    df["Issue"] = df["Description"].str.split(" ").str[0]
    df["Price"] = df["Price"].str.split("$").str[1]
    df = df.drop(["Weird", "Currency"], 1)

    df["Description"] = df["Description"].str.split(" ").str[1:]
    df["Name"] = df["Name"].str.strip()
    df["Name2"] = df["Name"].replace(" ", "_", regex=True)
    df["Release Date"] = pd.to_datetime(df["Release Date"])
    return df


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
    df = get_df_from_txt()
    for i in range(len(df.index)):
        if (
            df["Issue"].iloc[i] != None
        ):  # this way all TPBs and HC are thrown out, a more elegant way should be implemented
            issue_number = df["Issue"].iloc[i]
            comic_name = df["Name"].iloc[i]
            # comic_name_underscore = df["Name2"].iloc[i]
            publisher = df["Publisher"].iloc[i].capitalize()
            release_date = df["Release Date"].iloc[i]
            s, created = Series.objects.get_or_create(
                publisher=publisher,
                name=comic_name,
                volume=1,  # name_underscore=comic_name_underscore
            )
            c = Comic.objects.get_or_create(
                series=s, issue=issue_number, pub_date=release_date
            )


# importing of HC and TPB not implemented


def visualize_comics():
    df = pd.DataFrame(list(Comic.objects.all().values()))
    series_id_column = df["series_id"]
    new_id_column = []
    for i in range(len(series_id_column)):
        new_id_column.append(Series.objects.get(pk=series_id_column[i]).name)
    df = df.drop("series_id", axis=1)  # inplace = True
    df["series_name"] = pd.Series(new_id_column).values
    return df
