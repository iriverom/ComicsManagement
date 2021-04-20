from app.models import Client, Series, Suscription, Comic
from django.db.models import Count


def create_graph_data():
    context = {
        "test": "Popular Javascript Frameworks",
        "stars": [135850, 52122, 148825, 16939, 9763],
    }

    return context


def count_data(model, model_name):
    data_count = model.objects.annotate(num_subs=Count("suscription"))
    data = {}
    for element in data_count:
        if element.num_subs != 0:
            data[str(element)] = element.num_subs
    context = {
        f"labels_{model_name}_counts": list(data.keys())[:9],
        f"data_{model_name}_counts": list(data.values())[:9],
    }
    return context


def client_subscription_classification():
    data = count_data(Client, "client")
    value_set = list(set(data["data_client_counts"]))
    data_dict = {}
    for element in value_set:
        data_dict[f"customers with {str(element)} subscriptions"] = data[
            "data_client_counts"
        ].count(element)
    context = {
        "labels_client_counts": list(data_dict.keys())[:9],
        "data_client_counts": list(data_dict.values())[:9],
    }
    return context
