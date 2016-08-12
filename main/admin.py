from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

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
    exclude = ['uploaded_by',]
    
    # list_per_page = 10
    list_display = ('image_title', 'thumbnail')
    search_fields = ['image_title']
    
    actions = ['delete_selected_pics'] 
    def get_actions(self, request):
        actions = super(UpImagesModelAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    # Custom Bulk Delete. Also deletes the actual image files
    def delete_selected_pics(self, request, queryset): 
        for obj in queryset: obj.delete()
        if queryset.count() == 1:
                message_bit = "1 Εικόνα Διαγράφηκε"
        else:
                message_bit = "%s Εικόνες Διαγράφηκαν" % queryset.count()
        self.message_user(request, "%s Επιτυχώς." % message_bit)
    delete_selected_pics.short_description = "Διαγραφή Επιλεγμένων Εικόνων"
    
    # Fill in the "uploaded_by" field
    def save_model(self, request, obj, form, change):
        obj.uploaded_by = request.user
        obj.save()
admin.site.register(UpImages, UpImagesModelAdmin)

class PostsModelAdmin(admin.ModelAdmin):
	actions = ['publish']
	form = PostsForm
	# Which fields to display ( that's only for listview )
	list_display = ('title', 'pub_date','thumbnail', 'author', 'status', 'viewcount', 'category')
	#list_per_page = 10
	
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
	def get_form(self, request, obj=None, **kwargs):
		# If obj is not None it means we are in the change form
		# In that case hide "description"
		if obj:
			kwargs['exclude'] = ['description',]
		return super(BodyTextAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(BodyText, BodyTextAdmin)
