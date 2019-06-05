from collections import OrderedDict


def get_form_identifier_list_from_keys(form_list, form_keys):
    form_ids = [key for key, _ in form_list.items()]
    res = OrderedDict(zip(form_keys, form_ids))
    return {title: identifier for title, identifier in res.items()}
