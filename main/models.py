from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.html import mark_safe
from PIL import Image

import html
import datetime
import logging
logger = logging.getLogger('main')

class UpImages(models.Model):
    image = models.ImageField(blank=False, upload_to='images/%Y/%m/%d/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    image_title = models.CharField(blank=True, max_length=255, verbose_name='Τίτλος')

    def thumbnail(self):
        return u'<img src="%s"  style="max-width:150px; height:auto; max-height:150px;" />' % self.image.url
    thumbnail.short_description = 'Εικόνα'
    thumbnail.allow_tags = True
    
    def __str__(self):
        return self.image_title
    
    def save(self, *args, **kwargs):
        super(UpImages, self).save()
        imagepath = self.image.path
        image = Image.open(imagepath)
        image.save(imagepath, "JPEG", quality=30, optimize=True)
    
    def delete(self):
        if not self.image:
            self.image.delete()
        super(UpImages, self).delete()
    
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
    text = RichTextField("Κείμενο", blank=False)
    pub_date = models.DateTimeField('Ημερομηνία Ανάρτησης', default=datetime.datetime.now)
    image = models.ForeignKey(UpImages, on_delete=models.CASCADE, verbose_name='Εικόνα')
    title = models.CharField('Τίτλος' ,max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Αρθρογράφος')
    category = models.ForeignKey(Category,default=0, on_delete=models.CASCADE, verbose_name='Κατηγορία', blank=False)
    status = models.CharField('Κατάσταση', max_length=1, choices=STATUS_CHOICES, default='d')
    viewcount = models.IntegerField('Αριθμός Προβολών', default=0)

    def save(self, *args, **kwargs):
        # This is extremelly unsafe.
        self.text = html.unescape(self.text)
        super(Posts, self).save(*args, **kwargs)
    
    def thumbnail(self):
        return u'<img src="%s" id="thumb" style="max-width:150px; height:auto; max-height:150px;" />' % self.image.image.url
    thumbnail.short_description = 'Εικόνα Κειμένου'
    thumbnail.allow_tags = True
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Δημοσιεύσεις"
        verbose_name = "Δημοσίευση"
        ordering = ['-pub_date']


class BodyText(models.Model):
    text = models.TextField('Κείμενο', blank=False)
    description = models.CharField('Τοποθεσία Παρόντος Κειμένου', max_length=255)
    author = models.CharField('Ποίος Το Είπε', blank=False, max_length=255)
    
    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Κείμενο Σελίδας"
        verbose_name_plural = "Κείμενα Σελίδας"
