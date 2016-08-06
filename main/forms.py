from django import forms
from .models import Posts
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.auth.models import User


class PostsForm(forms.ModelForm):
	text = forms.CharField(widget=CKEditorUploadingWidget(), label='Κείμενο')
	# The id change on this form field is used to assist the "thumbnails.js" script
	class Meta:
		model = Posts
		exclude = ['pub_date', 'description', 'viewcount']
	# A script to dynamically change the thumbnails in Posts' change form using Ajax and JQuery
	class Media:
		js=('main/assets/js/thumbnails.js',)

