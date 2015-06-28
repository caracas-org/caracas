from . import views
from django.conf.urls import url

urlpatterns = [

    url(r'^overview/$', views.overview, name='overview'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),

]
