from django import template

register = template.Library()


@register.filter()
def censor(value):
    return value.replace('fuck', 'f**k').replace('Fuck', 'f**k')
