from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

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
	latest_posts = list(Posts.objects.exclude(status='d')[:3])
	if category_id is not None:
		category_posts = Posts.objects.filter(category=category_id).exclude(status='d').order_by('-viewcount')
		try:
			chosen_cat_name = Category.objects.get(pk=category_id)
		except ObjectDoesNotExist:
			raise Http404('Δεν υπάρχει αυτή η κατηγορία.')			
		if not category_posts:
			raise Http404('Δεν υπάρχουν δημοσιεύσεις σε αυτή την κατηγορία.')
	else:
		chosen_cat_name = "Στρόβιλος"
		category_posts = Posts.objects.exclude(Q(status='d')).order_by('-viewcount')
	
	# TODO: Uncomment this when we are ready to deploy
	# Check if the main posts are also recent posts so we don't show them twice
	# for post in category_posts:
	# 	if post in latest_posts:
	# 		try:
	# 			index = latest_posts.index(post)
	# 			del latest_posts[index]
	# 		except Exception as e:
	# 			print (e)

	paginator = Paginator(category_posts,settings.POSTS_PER_PAGE)
	page = request.GET.get('page')
	try:
		cat_post_paginated = paginator.page(page)
	except PageNotAnInteger:
		cat_post_paginated = paginator.page(1)
	except EmptyPage:
		cat_post_paginated = paginator.page(paginator.num_pages)
	
	view_context = {
		'chosen_cat_name'		: chosen_cat_name,
		'latest_posts'			: latest_posts,
		'cat_posts_paginated'	: cat_post_paginated,
	}
	base_cntx = get_base_context(form_errors)
	final_context = {**view_context, **base_cntx}
	return render(request, 'main/index.html',  final_context)

def articles(request, post_id):
	main_post = get_object_or_404(Posts ,pk=post_id)
	latest_posts = Posts.objects.exclude(Q(pk=main_post.id) | Q(status='d'))[:3]
	view_context = {
		'main_post'  : main_post,
		'latest_posts' : latest_posts,
	}
	base_cntx = get_base_context()
	final_context = {**view_context, **base_cntx}
	
	increasecnt(post_id)
	return render(request, 'main/left-sidebar.html', final_context)

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
    detail_fields = ['image_title']

    default_values = {}	

def handler404(request):
    response = render(request, 'main/404.html')
    response.status_code = 404
    return response

def handler500(request):
    response = render(request, 'main/500.html')
    response.status_code = 500
    return response
