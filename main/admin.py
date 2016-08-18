from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django import forms
from django_batch_uploader.admin import BaseBatchUploadAdmin
from .models import Posts, UpImages, Category, BodyText
from .forms import PostsForm

import logging
logger = logging.getLogger('main')

admin.site.index_title = ' '

admin.site.register(Category)

# model.save() method cannot does not have access to the request data structure 
# so this overriden method is the optimal way to change the 'uploaded_by' field 
class UpImagesModelAdmin(BaseBatchUploadAdmin):
    batch_url_name = "admin_image_batch_view"
    
    # This removes the following fields from both add and change forms
    exclude = ['uploaded_by','image_title', 'upload_date']
    
    list_display = ('upload_date', 'image_title', 'thumbnail')
    search_fields = ['image_title']

    def save_model(self, request, obj, form, change):
        obj.uploaded_by = request.user
        obj.save()
admin.site.register(UpImages, UpImagesModelAdmin)
class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.first_name
class PostsModelAdmin(admin.ModelAdmin):
	actions = ['publish']
	form = PostsForm
	# Which fields to display ( that's only for listview )
	list_display = ('title', 'thumbnail', 'category', 'author_name', 'status', 'viewcount', 'pub_date')
	
	# That also appears when changing the object
	readonly_fields = ('thumbnail',)
	search_fields = ['title']
	
	# Custom action to bulk publish posts 
	def publish(self, request, queryset):
		rows_updated = queryset.update(status='p')
		if rows_updated == 1:
			message_bit = "1  Άρθρο Δημοσιέυτηκε"
		else:
			message_bit = "%s Άρθρα Δημοσιεύτηκαν" % rows_updated
		self.message_user(request, "%s Επιτυχώς" % message_bit)
	publish.short_description = 'Δημοσίευση επιλεγμένων άρθρων'
	def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
		if db_field.name == 'author':
			kwargs['form_class'] = UserChoiceField
		return super(PostsModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
	def author_name(self, instance):
		return instance.author.first_name
	author_name.short_description = 'Αρθρογράφος'
admin.site.register(Posts, PostsModelAdmin)

# This is used to make some fields available in User Admin Forms
# Like first and last name
admin.site.unregister(User)

class UserModelAdmin(UserAdmin):
	# This is used to forbid other users to change permissions.
	# Therefore we hide the Permissions fields
	dad_fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        # No permissions
        (('Ημερομηνίες'), {'fields': ('last_login', 'date_joined')}),
    )

	# If you are staff hide the superuser record
	def get_queryset(self, request):
		qs = super(UserModelAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.exclude(is_superuser=True)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields' : ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')}
		),
	)
	def change_view(self, request, *args, **kwargs):
        # for non-superuser
		if not request.user.is_superuser:
			try:
				self.fieldsets = self.dad_fieldsets
				response = super(UserModelAdmin, self).change_view(request, *args, **kwargs)
			finally:
				# Reset fieldsets to its original value
				self.fieldsets = UserAdmin.fieldsets
			return response
		else:
			return super(UserModelAdmin, self).change_view(request, *args, **kwargs)

admin.site.register(User,UserModelAdmin)

class BodyTextAdmin(admin.ModelAdmin):
	list_display = ('text', 'author', 'pub_date')
	exclude = ['pub_date',]
admin.site.register(BodyText, BodyTextAdmin)
