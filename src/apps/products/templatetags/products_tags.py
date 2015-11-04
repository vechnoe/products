# coding: utf-8

from django import template

register = template.Library()


def can_like(obj, user_id):
    if not user_id:
        return False
    user_seq = [like.user_id for like in obj.all()]
    if not (user_id in user_seq):
        return True



@register.inclusion_tag('products/tags/like_button.html', takes_context=True)
def like_button(context, obj):
    user = context['request'].user
    _can_like = can_like(obj.likes, user.id)
    return dict(product=obj, can_like=_can_like)


