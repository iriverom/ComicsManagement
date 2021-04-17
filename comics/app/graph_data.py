from app.models import Client, Series, Suscription, Comic
from django.db.models import Count


def create_graph_data():
    context = {
        "test": "Popular Javascript Frameworks",
        "stars": [135850, 52122, 148825, 16939, 9763],
    }

    series_count = Series.objects.annotate(num_subs=Count("suscription"))
    data = {}
    for series in series_count:
        if series.num_subs != 0:
            data[str(series)] = series.num_subs
    context = {
        "labels_series_counts": list(data.keys())[:9],
        "data_series_counts": list(data.values())[:9],
    }
    return context

    # from app.graph_data import create_graph_data()
