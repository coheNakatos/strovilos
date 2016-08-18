from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from django_batch_uploader.views import AdminBatchUploadView
from .forms import ContactForm
from .models import Posts, UpImages, Category, BodyText
from .tasks import increasecnt, async_mail
from .utils import get_base_context
from strovilos import settings
import logging

logger = logging.getLogger('main')

def index(request, category_id=None):
	form_errors = None
	if request.method == 'POST':
		form = ContactForm(data=request.POST)
		if form.is_valid():
			# This is a honeypot field for spambots.
			# So if it's not empty, some spambot filled it in.	
			honeypot = form.cleaned_data['pot']
			if honeypot:
				logger.warn("Possible SpamBot Detected")
				return HttpResponseRedirect('/')			
			async_mail(form)
			messages.success(request, 'Επιτυχής Αποστολή. Σας Ευχαριστούμε.')
			return HttpResponseRedirect('/')
		else:
			form_errors = form.errors
	latest_posts = list(Posts.objects.exclude(status='d')[:5])
	try:
		quote = BodyText.objects.get(active=True)
	except ObjectDoesNotExist:
		quote = None
	
	if category_id is not None:
		posts = Posts.objects.filter(category=category_id).exclude(status='d').order_by('-viewcount')
		try:
			main_title = Category.objects.get(pk=category_id)
		except ObjectDoesNotExist:
			raise Http404('Δεν υπάρχει αυτή η κατηγορία.')			
		if not posts:
			raise Http404('Δεν υπάρχουν δημοσιεύσεις σε αυτή την κατηγορία.')
	else:
		main_title = "Στρόβιλος"
		posts = Posts.objects.exclude(Q(status='d')).order_by('-viewcount')
	
	# TODO: Uncomment this when we are ready to deploy
	# Check if the main posts are also recent posts so we don't show them twice
	# for post in posts:
	# 	if post in latest_posts:
	# 		try:
	# 			index = latest_posts.index(post)
	# 			del latest_posts[index]
	# 		except Exception as e:
	# 			print (e)

	paginator = Paginator(posts,settings.POSTS_PER_PAGE)
	page = request.GET.get('page')
	try:
		posts_paginated = paginator.page(page)
	except PageNotAnInteger:
		posts_paginated = paginator.page(1)
	except EmptyPage:
		posts_paginated = paginator.page(paginator.num_pages)
	
	view_context = {
		'main_title'			: main_title,
		'latest_posts'			: latest_posts,
		'posts_paginated'		: posts_paginated,
		'quote'					: quote,
	}
	base_cntx = get_base_context(form_errors)
	final_context = {**view_context, **base_cntx}
	return render(request, 'main/index.html',  final_context)

def articles(request, post_id):
	main_post = get_object_or_404(Posts ,pk=post_id)
	latest_posts = Posts.objects.exclude(Q(pk=main_post.id) | Q(status='d'))[:4]
	try:
		next_post = main_post.get_next_by_pub_date(category=main_post.category)
	except:
		next_post = None
	try:
		previous_post = main_post.get_previous_by_pub_date(category=main_post.category)
	except:
		previous_post = None
	view_context = {
		'main_post'  	: main_post,
		'latest_posts' 	: latest_posts,
		'next_post'		: next_post,
		'previous_post'	: previous_post,
	}
	base_cntx = get_base_context()
	final_context = {**view_context, **base_cntx}
	
	increasecnt(post_id)
	return render(request, 'main/left-sidebar.html', final_context)

def authors(request, author_id):
	author = User.objects.get(pk=author_id)
	posts = Posts.objects.filter(author__id=author_id).exclude(status='d').order_by('-viewcount')
	latest_posts = list(Posts.objects.filter(author__id=author_id).exclude(status='d')[:5])
	
	paginator = Paginator(posts,settings.POSTS_PER_PAGE)
	page = request.GET.get('page')
	try:
		posts_paginated = paginator.page(page)
	except PageNotAnInteger:
		posts_paginated = paginator.page(1)
	except EmptyPage:
		posts_paginated = paginator.page(paginator.num_pages)
	main_title = author.first_name + " " + author.last_name

	try:
		quote = BodyText.objects.get(active=True)
	except ObjectDoesNotExist:
		quote = None

	view_context = {
		'posts_paginated'	: posts_paginated,
		'latest_posts' 		: latest_posts,
		'main_title'		: main_title,
		'quote'				: quote,
	}

	base_cntx = get_base_context()
	final_context = {**view_context, **base_cntx}
	return render(request, 'main/index.html', final_context)	
def about(request):
	latest_posts = Posts.objects.exclude(status='d')[:3]
	view_context = {
		'latest_posts' : latest_posts,
	}
	base_cntx = get_base_context()
	final_context = {**view_context, **base_cntx}
	return render(request, 'main/about.html', final_context)

# This is used to dynamically change the thumbnails on Posts' change form, using ajax requests
def feed_ajax(request):
	image_title = request.GET['title']
	image = get_object_or_404(UpImages, image_title=image_title)
	return HttpResponse(image.image.url)



class ImageBatchView(AdminBatchUploadView):      

    model = UpImages

    #Media file name
    media_file_name = 'image'

    #Which fields can be applied in bulk?
    default_fields = []

    #Which fields can be applied individually?
    detail_fields = []

    default_values = {}	

def handler404(request):
    response = render(request, 'main/404.html')
    response.status_code = 404
    return response

def handler500(request):
    response = render(request, 'main/500.html')
    response.status_code = 500
    return response
