'''
With this you can do the following in a HTML template file:

{% load js %}
var x = "{{ some_context_var | js}}"; // This is a JSON representation of the variable

Not perfect or guarenteed to work in all scenarios, however it's a good way to send python
dicts as context variables and load them into javascript variables client-side.
'''
import json

from django.utils.safestring import mark_safe
from django.template import Library

register = Library()

@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))
