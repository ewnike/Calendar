from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index, name="index" ),
    url(r'^login$', views.login, name='login'),
    url(r'^register$',views.register, name='register'),
    url(r'^welcome$',views.homepage, name='homepage'),
    url(r'^home$', views.homepage, name="home"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^home$', views.homepage, name="home"),
    url(r'^add_appointment$', views.add_appointment, name='add_appointment'),
    url(r'^edit_appointment/(?P<id>\d+)$', views.edit_appointment, name="edit_appointment"),
    url(r'^delete_appointment/(?P<id>\d+)$', views.delete_appointment, name='delete_appointment'),

]
