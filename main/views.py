from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Posts, UpImages, Category, random_posts, BodyText
from .tasks import increasecnt 
from .utils import get_base_context
import logging

logger = logging.getLogger('main')

def index(request, category_id=None):
	categories = Category.objects.all()
	side_posts = list(Posts.objects.exclude(status='d')[:3])
	if category_id is not None:
		category_posts = get_list_or_404(Posts, ~Q(status='d') ,category=category_id)
		chosen_cat_name = get_object_or_404(Category, pk=category_id)
	else:
		chosen_cat_name = "Στροβιλος"
		category_posts = Posts.objects.exclude(Q(status='d'))
	
	# Check if the main posts are also recent posts so we don't show them twice
	# for post in category_posts:
	# 	if post in side_posts:
	# 		try:
	# 			index = side_posts.index(post)
	# 			del side_posts[index]
	# 		except Exception as e:
	# 			print (e)
	paginator = Paginator(category_posts,4)
	page = request.GET.get('page')
	try:
		cat_post_paginated = paginator.page(page)
	except PageNotAnInteger:
		cat_post_paginated = paginator.page(1)
	except EmptyPage:
		cat_post_paginated = paginator.page(paginator.num_pages)
	
	view_context = {
		'chosen_cat_name' : chosen_cat_name,
		'side_posts' : side_posts,
		'cat_posts_paginated' : cat_post_paginated,
		'categories' : categories,
	}
	base_cntx = get_base_context()
	final_context = {**view_context, **base_cntx}
	return render(request, 'main/index.html',  final_context)

def articles(request, post_id):
	main_post = get_object_or_404(Posts ,pk=post_id)
	side_posts = Posts.objects.exclude(Q(pk=main_post.id) | Q(status='d'))[:3]
	categories = Category.objects.all()
	view_context = {
		'main_post' : main_post,
		'side_posts' : side_posts,
		'categories' : categories,
	}
	base_cntx = get_base_context()
	final_context = {**view_context, **base_cntx}
	
	increasecnt(post_id)
	return render(request, 'main/left-sidebar.html', final_context)

def about(request):
	side_posts = Posts.objects.exclude(status='d')[:3]
	categories = Category.objects.all()
	view_context = {
		'side_posts' : side_posts,
		'categories' : categories,
	}
	base_cntx = get_base_context()
	final_context = {**view_context, **base_cntx}
	return render(request, 'main/about.html', final_context)

# This is used to dynamically change the thumbnails on Posts' change form, using ajax requests
def feed_ajax(request):
	image_title = request.GET['title']
	image = get_object_or_404(UpImages, image_title=image_title)
	return HttpResponse(image.image.url)


from django_batch_uploader.views import AdminBatchUploadView

class ImageBatchView(AdminBatchUploadView):      

    model = UpImages

    #Media file name
    media_file_name = 'image'

    #Which fields can be applied in bulk?
    default_fields = []

    #Which fields can be applied individually?
    detail_fields = ['image_title']

    default_values = {}	


