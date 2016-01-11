from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.LoginView.as_view(), name='card'),

    url(r'^pin/(?P<number>\d{16})/$', views.PinView.as_view(), name='pin'),

    url(r'^operations/$', views.OperationsView.as_view(), name='operations'),

    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
]
