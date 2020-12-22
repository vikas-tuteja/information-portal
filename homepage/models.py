from django.db import models

from category.models import Category
from content.models import Content, Library


# Create your models here.
class Configure(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField(Category, blank=True,
        help_text='Top categories to be displayed...')
    content = models.ManyToManyField(Content,
        help_text='Top n news/content...')
    library = models.ManyToManyField(Library,
        help_text='Top n audibles...')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Configure"
