from app.models import Client, Series, Subscription, Comic
from django.db.models import Count


def count_data(model, model_name, top):
    data_count = model.objects.annotate(num_subs=Count("subscription"))
    data = {}
    for element in data_count:
        if element.num_subs != 0:
            data[str(element)] = element.num_subs
    data = dict(sorted(data.items(), key=lambda item: item[1]))

    context = {
        f"labels_{model_name}_counts": list(data.keys())[-top:],
        f"data_{model_name}_counts": list(data.values())[-top:],
    }
    return context


def _client_subscription_classification():
    data = count_data(Client, "client", 0)
    value_set = list(set(data["data_client_counts"]))
    data_dict = {}
    for element in value_set:
        data_dict[f"Customers with {str(element)} subscriptions"] = data[
            "data_client_counts"
        ].count(element)

    context = {
        "labels_client_counts": list(data_dict.keys())[:9],
        "data_client_counts": list(data_dict.values())[:9],
    }

    return context
