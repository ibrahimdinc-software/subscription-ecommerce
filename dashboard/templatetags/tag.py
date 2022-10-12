from django import template

from django.template.loader import render_to_string

from addressapp.addressing import Address

register = template.Library()


@register.simple_tag
def getProvinceList():
    return Address().provList()


@register.simple_tag
def html_as_string(html):
    s = str(render_to_string(html))
    return s.encode().decode()


@register.filter
def dict_values(h, key):
    if key in h:
        return h[key]
    return ""
