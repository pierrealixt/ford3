from django import template
register = template.Library()


@register.filter
def index(form_list, i):
    return form_list[int(i)]
