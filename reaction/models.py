from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from myaccount.models import UserDetail
from content.models import Content, Library

# Create your models here.
class Reaction(models.Model):
    LIKE = 'Like'
    COMMENT = 'Comment'
    ACTIVITY_TYPES = (
        (COMMENT, COMMENT),
        (LIKE, LIKE),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserDetail, on_delete=models.CASCADE, verbose_name='Posted By')
    activity_type = models.CharField(max_length=10, choices=ACTIVITY_TYPES)
    text = models.CharField(max_length=255, blank=True, null=True)

    # Generic FK -> comment on Content, Library
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
        limit_choices_to = {'model__in': ['content', 'library']})
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    # comment on a comment, or like on a like 
    #reaction = models.ForeignKey('self', on_delete=models.CASCADE,
    #    blank=True, null=True, related_name='self_fk')
    

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'Likes & Comments'
