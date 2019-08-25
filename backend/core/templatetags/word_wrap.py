from django import template
import textwrap

register = template.Library()

@register.filter
def word_wrap(word, arg):
    """word wrap"""
    if not word:
        word=""
    return ' '.join(textwrap.wrap(str(word), arg))
