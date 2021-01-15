from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserDetail(models.Model):
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.BigIntegerField( unique=True )
    address = models.CharField( max_length=100, blank=True, null=True )

    def __str__(self):
        return self.auth_user.username

    class Meta:
        verbose_name_plural = "End Users"
