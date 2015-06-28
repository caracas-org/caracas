from . import views
from django.conf.urls import url

urlpatterns = [

    url(r'^overview/$', views.overview, name='overview'),

]
