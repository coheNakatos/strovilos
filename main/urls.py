from django.conf.urls import url
from . import views

app_name = 'main'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^articles/(?P<post_id>[0-9]+)$', views.articles, name='articles'),
    url(r'^categories/(?P<category_id>[0-9]+)$', views.index, name='categories'),
    url(r'^about/$', views.about, name='about'),
    url(r'^ajax/$', views.feed_ajax, name='ajax'),
]
