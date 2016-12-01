from django import template


register = template.Library()


@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})


@register.filter('klass')
def klass(ob):
    return ob.field.widget.__class__.__name__
