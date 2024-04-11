from django import template

register = template.Library()


@register.filter
def get_dict_item(dictionary, key):
    """_summary_.

    Args:
        dictionary: _description_
        key: _description_

    Returns:
        _description_
    """
    return dictionary.get(key)
