from django.conf.urls import url
from .views import LoginView, LogoutView

urlpatterns = [
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^login/$', LoginView.as_view(), name='login'),
]
