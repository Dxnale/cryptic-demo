from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="add_class")
def add_class(field, css_classes):
    """Return the field rendered with additional CSS classes.

    Usage in template:
      {{ field|add_class:"input input-bordered" }}
    """
    existing = field.field.widget.attrs.get("class", "").strip()
    combined = f"{existing} {css_classes}".strip() if existing else css_classes
    return field.as_widget(attrs={**field.field.widget.attrs, "class": combined})


@register.filter(name="label_class")
def label_class(field, css_classes):
    """Return the label tag for the field with CSS classes applied.

    Usage in template:
      {{ field|label_class:"label-text" }}
    """
    return mark_safe(field.label_tag(attrs={"class": css_classes}))
