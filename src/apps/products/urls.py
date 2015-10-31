# coding: utf-8

from django.conf.urls import patterns, url
from .views import ProductListView, ProductDetailView, send_like

urlpatterns = patterns(
    'products.views',
    url(r'products/$', ProductListView.as_view(), name='products_list'),
    url(r'products/(?P<slug>[\w-]+)/$',
        ProductDetailView.as_view(), name='product_detail'),
    url(r'send-like/$', send_like, name='like_create'),
)

