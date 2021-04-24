from app.models import Client, Series, Subscription, Comic
from django.db.models import Count


def create_graph_data():
    context = {
        "test": "Popular Javascript Frameworks",
        "stars": [135850, 52122, 148825, 16939, 9763],
    }

    return context


def count_data(model, model_name, top):
    data_count = model.objects.annotate(num_subs=Count("subscription"))
    data = {}
    for element in data_count:
        if element.num_subs != 0:
            data[str(element)] = element.num_subs
    newdata = dict(
        sorted(data.items(), key=lambda item: item[1])
    )  # if we don't sort the dict, the data we get in context is not ordered

    context = {
        f"labels_{model_name}_counts": list(newdata.keys())[-top:],
        f"data_{model_name}_counts": list(newdata.values())[-top:],
    }  # if we want the top 10, a 9 must be given
    return context


def _client_subscription_classification():
    data = count_data(Client, "client", 0)
    value_set = list(set(data["data_client_counts"]))
    data_dict = {}
    for element in value_set:
        data_dict[f"customers with {str(element)} subscriptions"] = data[
            "data_client_counts"
        ].count(element)

    newdata = dict(
        sorted(data_dict.items(), key=lambda item: item[1])
    )  # if we don't sort the dict, the data we get in context is not ordered

    context = {
        "labels_client_counts": list(data_dict.keys())[:9],
        "data_client_counts": list(data_dict.values())[:9],
    }  # the problem is probably here

    return context
