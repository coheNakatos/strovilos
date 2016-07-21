from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from django.utils.html import mark_safe
from random import randint
from django.db.models import Max, Q
import html
import datetime

class UpImages(models.Model):
    image = models.ImageField(blank=False, upload_to='images/%Y/%m/%d/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    image_title = models.CharField(blank=True, max_length=255, verbose_name='Τίτλος')

    def thumbnail(self):
        return u'<img src="%s" style="max-width:150px; height:auto; max-height:150px;" />' % self.image.url
    thumbnail.short_description = 'Εικόνα'
    thumbnail.allow_tags = True
    
    def __str__(self):
        return self.image_title

    class Meta:
        verbose_name = "Εικόνα"
        verbose_name_plural = "Εικόνες"

class Category(models.Model):
    name = models.CharField('Όνομα Κατηγορίας', max_length=100, default='Γενικά', blank=False)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural =  "Κατηγορίες"
        verbose_name = "Κατηγορία"

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
    description = models.CharField('Περιγραφή Κειμένου' ,max_length=100, default='Placeholder', blank=True)
    category = models.ForeignKey(Category,default=0, on_delete=models.CASCADE, verbose_name='Κατηγορία')
    status = models.CharField('Κατάσταση', max_length=1, choices=STATUS_CHOICES, default='d')
    #This is used to craft the short description of the post
    def trimwords(self, s, words):
        wordsinstr = s.split()
        # In case the text is smaller in wordcount that the description.Unlikely.
        if words > len(wordsinstr): 
            return ' '.join(wordsinstr)
        return(' '.join(s.split()[:words])) + '...</p>'

    def save(self, *args, **kwargs):
        self.description = self.trimwords((html.unescape(self.text)), 10)
        super(Posts, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def unescaped(self):
        return mark_safe(self.description)

    unescaped.short_description = description.verbose_name 
    class Meta:
        verbose_name_plural = "Δημοσιεύσεις"
        verbose_name = "Δημοσίευση"
        ordering = ['-pub_date']

def random_posts(model):
    TIMES = 10 
    posts = []
    max = model.objects.aggregate(Max('id'))['id__max']
    i = 0
    while i < TIMES:
        try:
            post = model.objects.get(Q(pk=randint(1, max)) & ~Q(status='d'))
            if post not in posts:
                posts.append(post)
        except model.DoesNotExist:
            pass
        i += 1
    return posts
