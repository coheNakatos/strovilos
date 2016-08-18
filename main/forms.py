from django import forms
from .models import Posts, UpImages
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.db.models.fields.related import ManyToOneRel
class PostsForm(forms.ModelForm):
	text = forms.CharField(widget=CKEditorUploadingWidget(), label='Κείμενο')
	# The id change on this form field is used to assist the "thumbnails.js" script
	class Meta:
		model = Posts
		exclude = ['viewcount']
	# A script to dynamically change the thumbnails in Posts' change form using Ajax and JQuery
	class Media:
		js=('main/assets/js/thumbnails.js',)

	# This is overriding the queryset during adding/changing a post
	def __init__(self, *args, **kwargs):
		super(PostsForm, self).__init__(*args, **kwargs)
		self.fields['image'].queryset = UpImages.objects.order_by('image_title')
class ContactForm(forms.Form):
	
	# Overriding the error_messages
	greek_errors_mail = {
		'required' : 'Αυτό το πεδίο είναι απαραίτητο',
		'invalid'  : 'Μη αποδεκτό email',
	}
	greek_errors = {
		'required' : 'Αυτό το πεδίο είναι απαραίτητο',
	}
	name = forms.CharField(required=True, error_messages=greek_errors)
	subject = forms.CharField(required=True, error_messages=greek_errors)
	email = forms.EmailField(required=True, error_messages=greek_errors_mail)
	message = forms.CharField(
		max_length = 500,
		required = True,
		error_messages = greek_errors,
		)
	# This is supposed to be empty.
	pot = forms.CharField(required=False)
