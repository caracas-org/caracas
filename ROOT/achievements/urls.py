
from . import views
from django.conf.urls import url

urlpatterns = [

    url(r'^api/unlock/$', views.UnlockProgress.as_view(), name='api'),
    url(r'^api/get/$', views.GetAchievements.as_view(), name='api'),
    url(r'^achievements/$', views.listAll, name='achievements'),

]
