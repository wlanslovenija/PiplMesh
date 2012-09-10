from django import template

register = template.Library()

@register.inclusion_tag('user/user_image.html', takes_context=True)
def user_image(context, user=None):
    if user is None:
        user = context['user']

    return {
        'user_image_url': user.get_image_url(),
    }

@register.simple_tag
def active(request, url_name):
    from django.core.urlresolvers import resolve 
    startswith = request.path.startswith('/'+url_name)
    resolved_name = resolve(request.path).url_name
    if startswith or url_name == resolved_name:
        return 'current_item'
    return ''
