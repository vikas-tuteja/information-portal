from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

from ckeditor_uploader.fields import RichTextUploadingField

from category.models import SubCategory

from utils.utils import validate_summary_len


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
    event_date = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    title = models.CharField(max_length=200, unique=True)
    content = RichTextUploadingField(
        config_name='special',
        external_plugin_resources=[(
                'youtube',
                '/media/ckeditor_plugins/ckeditor-youtube-plugin-master/youtube/',
                'plugin.js',
            )]
    )
    summary = models.TextField(
        help_text='Please enter a minimum of 180 characters',
        #validators=[validate_summary_len],
        blank=True, null=True
    )
    show_summary = models.BooleanField(default=True)
    summary_image = models.ImageField(upload_to=IMAGE_PATH, blank=True, null=True)
    watermark_image = models.ImageField(upload_to=IMAGE_PATH, blank=True, null=True)
    sub_category = models.ManyToManyField(SubCategory, blank=True)
    author = models.ForeignKey(User,
        on_delete=models.CASCADE, blank=True, null=True)
    views = models.IntegerField(default=0)

    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    approved_rejected_by = models.ForeignKey(User,
        on_delete=models.CASCADE,
        related_name='approved_rejected_by',
        blank=True, null=True)
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
    title = models.CharField(max_length=200, unique=True, help_text='Display name')
    audio_file = models.FileField(upload_to=AUDIO_PATH,
        help_text=("Allowed type - .mp3, .wav, .ogg"))
    size = models.FloatField(help_text='MB')
    filetype = models.CharField(max_length=10, help_text='file extension')
    summary = models.TextField(
        help_text='Please enter a minimum of 180 characters',
        #validators=[validate_summary_len],
        blank=True, null=True
    )
    show_summary = models.BooleanField(default=True)
    summary_image = models.ImageField(upload_to=IMAGE_PATH, blank=True, null=True)
    watermark_image = models.ImageField(upload_to=IMAGE_PATH, blank=True, null=True)
    sub_category = models.ManyToManyField(SubCategory, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)

    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    approved_rejected_by = models.ForeignKey(User,
        on_delete=models.CASCADE,
        related_name='Content_approved_rejected_by',
        blank=True, null=True)
    active_from = models.DateTimeField(blank=True, null=True)
    active_till = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.size = round(self.audio_file.size/(1024*1024),2)
        self.filetype = self.audio_file.name.split('.')[-1]
        if not self.pk:
            self.status = Status.objects.get(name='Pending')

        super(Library, self).save(*args, **kwargs)

    class Meta:
        db_table = "library"
        verbose_name_plural = "Library"
