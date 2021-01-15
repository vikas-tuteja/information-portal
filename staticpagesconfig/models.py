from django.db import models

# Create your models here.
class FAQs(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    question = models.CharField(max_length=255)
    answer = models.TextField()
    position = models.IntegerField()
    active = models.BooleanField()

    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = "FAQs Config"
