from django import template

register = template.Library()

@register.filter
def field_label(form, field_name):
    try:
        return form[field_name].label
    except KeyError:
        return field_name
