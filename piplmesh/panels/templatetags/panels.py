from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def render_panel(context, panel):
    context.push()
    request = context['request']
    output = panel.render(request, context)
    context.pop()
    return output
