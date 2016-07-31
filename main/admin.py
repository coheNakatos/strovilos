from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Posts, UpImages, Category
from .forms import UpImagesForm, PostsForm
from django_batch_uploader.admin import BaseBatchUploadAdmin

admin.site.index_title = ' '

admin.site.register(Category)

# model.save() method cannot does not have access to the request data structure 
# so this overriden method is the optimal way to change the 'uploaded_by' field 
class UpImagesModelAdmin(BaseBatchUploadAdmin):
    def save_model(self, request, obj, form, change):
        obj.uploaded_by = request.user
        obj.save()
    batch_url_name = "admin_image_batch_view"
    form = UpImagesForm
    list_per_page = 10
    list_display = ('image_title', 'thumbnail')
    search_fields = ['image_title']
admin.site.register(UpImages, UpImagesModelAdmin)

class PostsModelAdmin(admin.ModelAdmin):
	actions = ['publish']
	form = PostsForm
	# Which fields to display ( that's only for listview ) . 'unescaped' is a custom field to unescape html
	list_display = ('title', 'pub_date','thumbnail', 'unescaped', 'author', 'status')
	#list_per_page = 10
	# That also appears when changing the object
	readonly_fields = ('thumbnail',)
	search_fields = ['title']
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
	def get_queryset(self, request):
		qs = super(UserModelAdmin, self).get_queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.exclude(username='coheNakatos')
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

