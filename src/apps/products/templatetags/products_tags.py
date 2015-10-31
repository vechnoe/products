# coding: utf-8

from django import template
from django.contrib.auth.models import User

register = template.Library()


def can_like(obj, user):
    user = User.objects.filter(username=user)
    if not user.exists():
        return False
    return obj.can_like(user.first())


@register.inclusion_tag('products/tags/like_button.html', takes_context=True)
def like_button(context, obj):
    user = context['request'].user
    _can_like = can_like(obj, user)
    return dict(product=obj, user=user, can_like=_can_like)


