from django import template

register = template.Library()


# creation de filtres perso
@register.filter
def model_type(value):
    return type(value).__name__


@register.filter
def get_range(value):
    return range(value)


@register.filter
def get_complement(value):
    return range(5 - value)


@register.simple_tag(takes_context=True)
def get_poster_display(context, user):
    if user == context["user"]:
        return "Vous"
    return user.username
