from django.contrib.auth.models import User
from django.db import models
from django.utils.html import mark_safe
from django.core.urlresolvers import reverse

from ckeditor.fields import RichTextField
from bs4 import BeautifulSoup
from PIL import Image

import html, datetime, logging

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
        # Setting image title and reducing image quality.
        self.image_title = (self.image.path).split('/')[-1].split('.')[0]
        super(UpImages, self).save(*args, **kwargs)
        imagepath = self.image.path
        image = Image.open(imagepath)
        image.save(imagepath, "JPEG", quality=20)
    
    
    class Meta:
        verbose_name = "Εικόνα"
        verbose_name_plural = "Εικόνες"
        ordering = ['-upload_date']

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
    text = RichTextField("Κείμενο", blank=False)
    pub_date = models.DateField('Ημερομηνία Ανάρτησης', default=datetime.date.today)
    image = models.ForeignKey(UpImages, on_delete=models.SET_NULL, null=True, verbose_name='Εικόνα')
    title = models.CharField('Τίτλος' ,max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Αρθρογράφος')
    category = models.ForeignKey(Category,default=0, on_delete=models.CASCADE, verbose_name='Κατηγορία', blank=False)
    status = models.CharField('Κατάσταση', max_length=1, choices=STATUS_CHOICES, default='d')
    viewcount = models.IntegerField('Αριθμός Προβολών', default=0)
    
    
    def thumbnail(self):
        return u'<img src="%s" id="thumb" style="max-width:150px; height:auto; max-height:150px;" />' % self.image.image.url
    thumbnail.short_description = 'Εικόνα Κειμένου'
    thumbnail.allow_tags = True
    
    def show_link(self):
        return '<a href="%s"> Προβολή Άρθρου </a>' % self.get_absolute_url()
    show_link.allow_tags = True
    show_link.short_description = "-"
    
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
    author = models.CharField('Ποίος Το Είπε', blank=False, max_length=255)
    active = models.BooleanField(verbose_name='Ενεργό', default=False)
    pub_date = models.DateTimeField('Ημερομηνία Αρχικής Δημοσίευσης', default=datetime.datetime.now)


    def activate(self):
        # This is used to activate a quote through the changelist
        return "<a href='/activate?q=" + str(self.id) + "' class='grp-add-link grp-state-focus'> Ενεργοποίηση </a> "
    activate.allow_tags = True
    activate.short_description = "Ενεργοίηση Παραφοράς"

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



# Overring User's str method
def user_str_patch(self):
    return self.first_name

User.__str__ = user_str_patch