from django.template.defaulttags import register


@register.filter
def tabindex(value, index):
    """Adds a custom template tag.

    This adds a tabindex on a input field. The tabindex decides where the cursor will
    go next when 'tab' is pressed. Example::

        {{form.description | tabindex: 0}}

    Will be converted to something like::

        <input type=text name="description" tabindex=0>

    Add a tabindex attribute to the widget for a bound field.
    """
    value.field.widget.attrs["tabindex"] = index
    return value
