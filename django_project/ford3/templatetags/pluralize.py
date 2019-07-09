from django import template

register = template.Library()


@register.filter
def pluralize(number, singular = '', plural = 's'):
    if number == 1:
        return singular
    else:
        return plural
