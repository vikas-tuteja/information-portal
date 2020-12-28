from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

from ckeditor.fields import RichTextField

from category.models import SubCategory


# Create your models here.
IMAGE_PATH = 'content/images/'
class Image(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to=IMAGE_PATH)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "images"
        verbose_name_plural = "Images for inner content"

class Status(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Status"


class Content(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    title = models.CharField(max_length=200, unique=True)
    content = RichTextField()
    summary = models.TextField(blank=True, null=True,
        help_text='If left blank, first 200 characters \
            from content will be displayed as summary.')
    summary_image = models.ImageField(upload_to=IMAGE_PATH, blank=True, null=True)
    sub_category = models.ManyToManyField(SubCategory, blank=True)
    author = models.ForeignKey(User,
        on_delete=models.CASCADE, blank=True, null=True)
    views = models.IntegerField(default=0)

    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    active_from = models.DateTimeField(blank=True, null=True)
    active_till = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if not self.pk:
            self.status = Status.objects.get(name='Pending')

        super(Content, self).save(*args, **kwargs)

    class Meta:
        db_table = "content"


AUDIO_PATH = 'content/library'
class Library(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    title = models.CharField(max_length=200, unique=True)
    audio_file = models.FileField(
        help_text=("Allowed type - .mp3, .wav, .ogg"))
    summary = models.TextField(blank=True, null=True)
    summary_image = models.ImageField(upload_to=IMAGE_PATH, blank=True, null=True)
    sub_category = models.ManyToManyField(SubCategory, blank=True)
    author = models.ForeignKey(User,
        on_delete=models.CASCADE, blank=True, null=True)
    views = models.IntegerField(default=0)

    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    active_from = models.DateTimeField(blank=True, null=True)
    active_till = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if not self.pk:
            self.status = Status.objects.get(name='Pending')

        super(Library, self).save(*args, **kwargs)

    class Meta:
        db_table = "library"
        verbose_name_plural = "Library"
