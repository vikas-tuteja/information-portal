from django.db import models

from category.models import Category
from content.models import Content, Library


# Create your models here.
class Configure(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    articles = models.ManyToManyField(Content, blank=True,
        related_name='content_articles',
        limit_choices_to={'active': True,
            'sub_category__category__slug': 'articles'},
        help_text='Top articles to be displayed.')
    blogs = models.ManyToManyField(Content, blank=True,
        related_name='blogs_articles',
        limit_choices_to={'active': True,
            'sub_category__category__slug': 'blogs'},
        help_text='Top blogs to be displayed.')
    news = models.ManyToManyField(Content, blank=True,
        related_name='news_articles',
        limit_choices_to={'active': True,
            'sub_category__category__slug': 'news'},
        help_text='Top categories to be displayed...')
    library = models.ManyToManyField(Library, blank=True,
        limit_choices_to={'active': True},
        help_text='Top n audibles...')

    objects_count = models.IntegerField(default=10,
        help_text='The no. of objects in each section')

    articles_section = models.BooleanField(default=True, help_text='Show/Hide Articles Section on Home page')
    blogs_section = models.BooleanField(default=True, help_text='Show/Hide blogs Section on Home page')
    news_section = models.BooleanField(default=True, help_text='Show/Hide News Section on Home page')
    library_section = models.BooleanField(default=True, help_text='Show/Hide Library Section on Home page')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Configure"
