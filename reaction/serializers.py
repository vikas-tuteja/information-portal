from rest_framework import serializers

from reaction.models import Reaction
from myaccount.serializers import UserNameSerializer


class CommentListSerializers( serializers.ModelSerializer ):
    user = UserNameSerializer()
    #likes = serializers.SerializerMethodField(method_name='likes_on_comments')
    #comments = serializers.SerializerMethodField(method_name='comment_on_comments')

    class Meta:
        model = Reaction
        #fields = ('id', 'user', 'created_at', 'text', 'likes', 'comments')
        fields = ('id', 'user', 'created_at', 'text')

    """def likes_on_comments(self, obj):
        return self.Meta.model.objects.filter(
            activity_type='Like',
            reaction=obj
        ).count()

    def comment_on_comments(self, obj):
        return self.Meta.model.objects.filter(
            activity_type='Comment',
            reaction=obj
        ).values_list('text', 'user__auth_user__first_name',
            'user__auth_user__last_name', 'created_at')
    """

class ReactionCreateSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Reaction
        fields = ('user', 'content_type', 'object_id', 'activity_type', 'text')


class ReactionEditSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Reaction
        fields = ('text',)
