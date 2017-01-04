from django import template
from rank.models import Category

register = template.Library()


@register.inclusion_tag('rank/cats.html')
def get_categories(cat=None):
    return {'cats': Category.objects.all(), 'act_cat': cat}
