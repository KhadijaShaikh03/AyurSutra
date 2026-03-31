from django import template

register = template.Library()

@register.filter
def has_patient(user):
    return hasattr(user, 'patient')
