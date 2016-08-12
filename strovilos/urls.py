from django.conf.urls import url, include
from django.contrib import admin
from main.views import ImageBatchView

urlpatterns = [
    url(r'^', include('main.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url( r'admin/media/images/batch/$', ImageBatchView.as_view(), name="admin_image_batch_view"),     
]
handler404 = 'main.views.handler404'

handler500 = 'main.views.handler500'