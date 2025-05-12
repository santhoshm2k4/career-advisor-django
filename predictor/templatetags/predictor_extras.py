# predictor/templatetags/predictor_extras.py
from django import template

register = template.Library()

@register.filter(name='get')
def get_item(dictionary, key):
    """Allows accessing dictionary items with a variable key in templates.
       Returns None if key is not found or dictionary is not valid.
    """
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None

# You can add other custom filters here if needed