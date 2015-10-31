from django.conf.urls import include, url
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('products.urls', namespace='products')),
    url(r'^', include('users.urls', namespace='users')),
    url(r'^$', RedirectView.as_view(permanent=True,
        url=reverse_lazy('products:products_list')), name='home'),
]
