from django import template

register = template.Library()


@register.filter()
def checked_or_crossed(value):
    return '&#9989' if value else '&#10060'


@register.filter()
def is_none(value):
    return '<span class="pl-2 text-muted">Not specified yet</span>' \
        if value is None else value


@register.filter()
def is_number_none(value):
    return '<span class="pl-2 text-muted">0</span>' \
        if value is None else value
