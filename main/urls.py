from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

#####################################################
############### Main Url Configuration ##############
#####################################################

app_name = 'main'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^articles/(?P<post_id>[0-9]+)$', views.articles, name='articles'),
    url(r'^categories/(?P<category_id>[0-9]+)$', views.index, name='categories'),
    url(r'^authors/(?P<author_id>[0-9]+)$', views.authors, name='authors'),
    url(r'^about/$', views.about, name='about'),
    url(r'^ajax/get-title$', views.get_title, name='get-title'),
    url(r'^ajax/update-cvs$', views.update_cvs, name='update-cvs'),
    url(r'^secret/$', views.secret_articles, name='secret'),
    url(r'^activate/$', views.activate, name='activate')
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)