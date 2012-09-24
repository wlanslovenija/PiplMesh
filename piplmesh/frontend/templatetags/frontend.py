from django import template

register = template.Library()

@register.filter()
def is_active(current_path, url_path):
    return current_path.startswith(url_path)
