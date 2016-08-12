from django.conf import settings

"""
	Custom Context Processor
	Add here any settings fields
	you need in templates.
"""
def global_settings(request):
    # return any necessary values
    return {
        'TITLE_COUNT': settings.TITLE_COUNT,
        'DESC_COUNT': settings.DESC_COUNT,
    }
