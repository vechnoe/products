from django.contrib import admin
from django.contrib.admin.views import main
from django.core.urlresolvers import reverse

from .models import Product, Comment, Like


class ProductAdmin(admin.ModelAdmin):
    def view_on_site(self, object):
        return reverse('products:product_detail', kwargs={'slug': object.slug})

    def view_on_site_button(self, object):
        return '<a href="%s">View on site</a>' % self.view_on_site(object)

    view_on_site_button.allow_tags = True
    view_on_site_button.short_description = ''
    list_display = ('name', 'view_on_site_button')


class CommentAdmin(admin.ModelAdmin):
    def __init__(self, *args, **kwargs):
        super(CommentAdmin, self).__init__(*args, **kwargs)
        main.EMPTY_CHANGELIST_VALUE = 'Anonimous'
    list_display = ('user', 'created_at', 'product')

admin.site.register(Product, ProductAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like)