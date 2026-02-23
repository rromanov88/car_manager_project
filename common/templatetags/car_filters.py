from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='currency')
def currency(value):
    """
    Format a number as currency: € 1,250.50
    """
    try:
        value = float(value)
        return f"€ {value:,.2f}"
    except (ValueError, TypeError):
        return value


@register.filter(name='km')
def km(value):
    """
    Format a number as distance: 150,000 km
    """
    try:
        value = int(value)
        return f"{value:,} km"
    except (ValueError, TypeError):
        return value


@register.filter(name='color_badge')
def color_badge(value):
    """
    Return a Bootstrap badge with the car's color.
    Returns safe HTML.
    """
    if not value:
        return ""
    
    # Try to determine if we should use light or dark text based on simple color mapping
    dark_colors = ['black', 'blue', 'navy', 'purple', 'darkgrey', 'green', 'brown']
    text_color = "white"
    if value.lower() in ['white', 'yellow', 'lightgrey', 'silver', 'pink', 'gold']:
        text_color = "black"
        
    return mark_safe(f'<span class="badge" style="background-color: {value}; color: {text_color}; border: 1px solid #dee2e6;">{value}</span>')
