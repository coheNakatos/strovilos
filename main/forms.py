from django import forms
from .models import Posts
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostsForm(forms.ModelForm):
	text = forms.CharField(widget=CKEditorUploadingWidget(), label='Κείμενο')
	# The id change on this form field is used to assist the "thumbnails.js" script
	class Meta:
		model = Posts
		exclude = ['pub_date', 'description', 'viewcount']
	# A script to dynamically change the thumbnails in Posts' change form using Ajax and JQuery
	class Media:
		js=('main/assets/js/thumbnails.js',)

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