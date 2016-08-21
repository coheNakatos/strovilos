from django.conf.urls import url, include
from django.contrib import admin
from main.views import ImageBatchView
from django.shortcuts import render


#####################################################
############### Project Url Configuration ###########
#####################################################

urlpatterns = [
    url(r'^', include('main.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url( r'admin/media/images/batch/$', ImageBatchView.as_view(), name="admin_image_batch_view"),     
]

#####################################################
############### Custom Error Handling ###############
#####################################################

def custom_handler404(request):
    response = render(request, 'main/404.html')
    response.status_code = 404
    return response
handler404 = custom_handler404

def custom_handler500(request):
    response = render(request, 'main/500.html')
    response.status_code = 500
    return response

handler500 = custom_handler500

