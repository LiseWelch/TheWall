from django.conf.urls import url
from . import views

urlpatterns =[
    url(r'^$', views.root),
    url(r'^wall$', views.wall),
    url(r'^post$', views.post),
    url(r'^comment$', views.comment),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'delete/(?P<type>message)/(?P<id>[1-9]+[0-9]*)$', views.delete),
    url(r'delete/(?P<type>comment)/(?P<id>[1-9]+[0-9]*)$', views.delete)
]