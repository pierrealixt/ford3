from django import template
from ford3.enums.saqa_qualification_level import SaqaQualificationLevel

register = template.Library()


@register.filter()
def filter_level(value):
    try:
        level = value.split('.')[1]
        return SaqaQualificationLevel[level].value
    except:
        return None
