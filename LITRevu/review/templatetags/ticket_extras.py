from django import template

register = template.Library()

@register.filter
def model_type(value):
    return type(value).__name__

@register.filter
def get_range(value):
    return range(value)

@register.filter
def get_complement(value):
    return range(5 - value)
