from django import forms
from .models import UpImages, Posts
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.models import User

class UpImagesForm(forms.ModelForm):

    class Meta:
        model = UpImages
        exclude = ['uploaded_by']

class PostsForm(forms.ModelForm):
	text = forms.CharField(widget=CKEditorWidget(), label='Κείμενο')
	class Meta:
		model = Posts
		exclude = ['pub_date','description']

