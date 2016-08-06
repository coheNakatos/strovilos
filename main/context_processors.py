from .models import UpImages, BodyText


def logo_and_bodytexts(request):
	logo = UpImages.objects.get(image_title="Logo")	
	quote = BodyText.objects.get(description='Γνωμικό')
	return {'logo': logo, 'quote': quote}