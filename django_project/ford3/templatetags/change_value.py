from django import template

register = template.Library()


@register.filter()
def is_none(value):
    return '<span class="text-muted">Not specified yet</span>' \
        if value is None else value
