from bs4 import BeautifulSoup
import re

from django import template
from django.templatetags import static
from django.utils.text import slugify, mark_safe

register = template.Library()


class FullStaticNode(static.StaticNode):
    def url(self, context):
        request = context['request']
        return request.build_absolute_uri(super().url(context))


@register.tag
def static_absolute(parser, token):
    return FullStaticNode.handle_token(parser, token)


def build_anchor_id(element, suffix):
    return slugify(get_label(element) + suffix)


def get_label(element):
    return re.sub(r'^.* \- ', '', element.contents[0])


@register.filter
def add_anchors(value, suffix=''):
    soup = BeautifulSoup(value, 'html.parser')
    for element in soup.findAll('h2'):
        element.attrs['id'] = build_anchor_id(element, suffix)
    return mark_safe(str(soup))


@register.filter
def add_export_elements_classes(value):
    soup = BeautifulSoup(value, 'html.parser')
    mapping = [
        ('h1', 'heading-xlarge'),
        ('h2', 'heading-large'),
        ('h3', 'heading-medium'),
        ('h4', 'heading-small'),
        ('h5', 'heading-small'),
        ('h6', 'heading-small'),
        ('ul', 'list list-bullet'),
        ('ol', 'list list-number'),
        ('p', 'body-text'),
        ('a', 'link'),
        ('blockquote', 'quote'),
    ]
    for tag_name, class_name in mapping:
        for element in soup.findAll(tag_name):
            element.attrs['class'] = class_name
    return mark_safe(str(soup))
