from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse
from .models import Posts, UpImages, Category, random_posts
import logging
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
logger = logging.getLogger('django')

def index(request, category_id=None):
	logo = UpImages.objects.get(image_title="Logo")
	categories = Category.objects.all()
	side_posts = list(Posts.objects.exclude(status='d')[:3])
	#TODO: needs pagination
	if category_id is not None:
		category_posts = get_list_or_404(Posts, ~Q(status='d') ,category=category_id)
		chosen_cat_name = get_object_or_404(Category, pk=category_id)
	else:
		chosen_cat_name = "Στροβιλος"
		category_posts = random_posts(Posts)
	
	# Check if the main posts are also recent posts so we don't show them twice
	for post in category_posts:
		if post in side_posts:
			try:
				index = side_posts.index(post)
				del side_posts[index]
			except Exception as e:
				print (e)
	paginator = Paginator(category_posts,2)
	page = request.GET.get('page')
	try:
		cat_post_paginated = paginator.page(page)
	except PageNotAnInteger:
		cat_post_paginated = paginator.page(1)
	except EmptyPage:
		cat_post_paginated = paginator.page(paginator.num_pages)
	print (side_posts)
	return render(request, 'main/index.html', {'chosen_cat_name' : chosen_cat_name, 'side_posts' : side_posts, 'cat_posts_paginated' : cat_post_paginated, 'logo' : logo, 'categories': categories})

def articles(request, post_id):
	logo = UpImages.objects.get(image_title="Logo")	
	main_post = get_object_or_404(Posts ,pk=post_id)
	side_posts = Posts.objects.exclude(Q(pk=main_post.id) | Q(status='d'))[:3]
	categories = Category.objects.all()
	for post in side_posts:
		print (post.status)
	return render(request, 'main/left-sidebar.html', {'main_post': main_post ,'side_posts' : side_posts, 'logo' : logo, 'categories': categories})

def about(request):
	logo = UpImages.objects.get(image_title="Logo")
	side_posts = Posts.objects.exclude(status='d')[:3]
	categories = Category.objects.all()
	return render(request, 'main/about.html', {'side_posts': side_posts, 'logo' : logo, 'categories': categories})