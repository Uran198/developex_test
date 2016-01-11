from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.CardView.as_view(), name='card'),
]
