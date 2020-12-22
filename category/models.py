from django.db import models
from django.utils.text import slugify

IMAGE_PATH = 'category/images/'
# Create your models here.
class Category(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    active = models.BooleanField(default=True)

    active_from = models.DateTimeField(blank=True, null=True)
    active_till = models.DateTimeField(blank=True, null=True)

    image = models.ImageField(upload_to=IMAGE_PATH, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        db_table = "category"

class SubCategory(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    active = models.BooleanField(default=True)
    category = models.ManyToManyField(Category)

    active_from = models.DateTimeField(blank=True, null=True)
    active_till = models.DateTimeField(blank=True, null=True)

    image = models.ImageField(upload_to=IMAGE_PATH, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(SubCategory, self).save(*args, **kwargs)

    class Meta:
        db_table = "sub_category"
