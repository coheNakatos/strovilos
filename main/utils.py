from .models import UpImages, BodyText

def get_base_context():
		logo = UpImages.objects.get(image_title="Logo")	
		quote = BodyText.objects.get(description='Γνωμικό')
		context = {'logo': logo, 'quote': quote}
		return context