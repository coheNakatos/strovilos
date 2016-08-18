from django.contrib.auth.models import User
from django.db import models
from django.utils.html import mark_safe
from django.dispatch import receiver
from django.core.urlresolvers import reverse

from ckeditor.fields import RichTextField
from bs4 import BeautifulSoup
from PIL import Image

import html, datetime, logging, re, os

logger = logging.getLogger('main')

class UpImages(models.Model):
    image = models.ImageField(blank=False, upload_to='images/%Y/%m/%d/', max_length=250)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    image_title = models.CharField(blank=True, max_length=255, verbose_name='Τίτλος')
    upload_date = models.DateTimeField('Ημερομηνία Ανάρτησης', default=datetime.datetime.now)


    def thumbnail(self):
        return u'<img src="%s"  style="max-width:150px; height:auto; max-height:150px;" />' % self.image.url
    thumbnail.short_description = 'Εικόνα'
    thumbnail.allow_tags = True
    
    def __str__(self):
        return self.image_title
    
    def save(self, *args, **kwargs):
        self.image_title = (self.image.path).split('/')[-1].split('.')[0]
        super(UpImages, self).save(*args, **kwargs)
        imagepath = self.image.path
        image = Image.open(imagepath)
        # Reduce quality in the future
        image.save(imagepath, "JPEG", quality=20)
    
    
    class Meta:
        verbose_name = "Εικόνα"
        verbose_name_plural = "Εικόνες"

class Category(models.Model):
    name = models.CharField('Όνομα Κατηγορίας', max_length=100, blank=False)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Κατηγορία"
        verbose_name_plural =  "Κατηγορίες"

class Posts(models.Model):
    STATUS_CHOICES = (
        ('p', 'Δημοσιευμένο'),
        ('d', 'Πρόχειρο'),
    )
    POST_TYPES = (
        ('o', 'Παλιό'),
        ('n', 'Καινούργιο')
    )
    text = RichTextField("Κείμενο", blank=False)
    pub_date = models.DateField('Ημερομηνία Ανάρτησης', default=datetime.date.today)
    image = models.ForeignKey(UpImages, on_delete=models.CASCADE, verbose_name='Εικόνα')
    title = models.CharField('Τίτλος' ,max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Αρθρογράφος')
    category = models.ForeignKey(Category,default=0, on_delete=models.CASCADE, verbose_name='Κατηγορία', blank=False)
    status = models.CharField('Κατάσταση', max_length=1, choices=STATUS_CHOICES, default='d')
    viewcount = models.IntegerField('Αριθμός Προβολών', default=0)
    post_type = models.CharField('Είδος Δημοσίευσης', max_length=1, choices=POST_TYPES, default='o')
    def save(self, *args, **kwargs):
        if self.post_type == 'o':
            p = re.compile('[0-9]{3,4}x[0-9]{3,4}.*$')
            static_path = '/media/images/2016/08/15/'
            soup = BeautifulSoup(self.text)
            for img in soup.findAll('img'):
                # Make Images Responsive
                img['style'] = "width: 100%; height: auto;"
                if 'wp-content' in img['src']:
                    splits = img['src'].split('/')
                    logger.warn(splits)
                    year = splits[5]
                    month = splits[6]
                    filename = splits[7]
                    if p.search(filename) is not None:
                        format = filename.split('.')[-1]
                        filename = '-'.join(filename.split('-')[:-1]) + "." + format        
                    final_path = static_path + year + "_" + month + "_" + filename 
                    img['src'] = final_path
            for a in soup.findAll('a'):
                if  'wp-content' in a['href']:
                    splits = a['href'].split('/')
                    year = splits[5]
                    month = splits[6]
                    filename = splits[7]
                    final_path = static_path + year + "_" + month + "_" + filename 
                    a['href'] = final_path
            self.text = str(soup)
            logger.warn(soup)
            self.post_type = 'n'
        super(Posts, self).save(*args, **kwargs)
    def thumbnail(self):
        return u'<img src="%s" id="thumb" style="max-width:150px; height:auto; max-height:150px;" />' % self.image.image.url
    thumbnail.short_description = 'Εικόνα Κειμένου'
    thumbnail.allow_tags = True
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('main:articles', args=(self.id,))
    class Meta:
        verbose_name_plural = "Δημοσιεύσεις"
        verbose_name = "Δημοσίευση"
        ordering = ['-pub_date']


class BodyText(models.Model):
    text = models.TextField('Κείμενο', blank=False)
    #description = models.CharField('Περιγραφή Γνωμικού', blank=False, max_length=100)
    author = models.CharField('Ποίος Το Είπε', blank=False, max_length=255)
    active = models.BooleanField(verbose_name='Ενεργό', default=False)
    pub_date = models.DateTimeField('Ημερομηνία Αρχικής Δημοσίευσης', default=datetime.datetime.now)
    def __str__(self):
        return self.text + " ------- " + self.author

    def save(self, *args, **kwargs):
        if self.active == True:
            try:
                current_active = BodyText.objects.get(active=True)
                if self != current_active:
                    current_active.active = False;
                    current_active.save()
            except BodyText.DoesNotExist:
                pass
        super(BodyText, self).save(*args, **kwargs)


    class Meta:
        verbose_name_plural = "Παραφορές"
        verbose_name = "Παραφορά"



@receiver(models.signals.post_delete, sender=UpImages)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `UpImages` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
