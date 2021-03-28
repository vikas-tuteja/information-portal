from django.contrib import admin

from reaction.models import Reaction

# Register your models here.
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'object_id', 'activity_type', 'user', 'text')

admin.site.register(Reaction, ReactionAdmin)
