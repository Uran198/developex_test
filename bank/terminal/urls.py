from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.LoginView.as_view(), name='card'),

    url(r'^pin/(?P<number>\d{16})/$', views.PinView.as_view(), name='pin'),

    url(r'^operations/$', views.OperationsView.as_view(), name='operations'),

    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),

    url(r'^withdraw/$', views.WithdrawMoneyView.as_view(), name='withdraw'),

    url(r'^balance/$', views.ShowBalanceView.as_view(), name='balance'),

    url(r'^result/(?P<pk>[0-9]+)/$', views.OperationResultView.as_view(), name='result'),
]
