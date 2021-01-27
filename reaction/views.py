from rest_framework import generics
from rest_framework import permissions

from django.contrib.contenttypes.models import ContentType

from reaction.models import Reaction
from myaccount.models import UserDetail

from reaction.serializers import CommentListSerializers, ReactionCreateSerializer, ReactionEditSerializer
# Create your views here.
class CommentListByPost( generics.ListAPIView ):
    permission_classes = []
    serializer_class = CommentListSerializers

    def get_queryset(self, *args, **kwargs):
        content_type = self.kwargs['post_type']
        object_id = self.kwargs['post_id']

        self.common_filters = {
            'content_type': ContentType.objects.get(model=content_type),
            'object_id': object_id,
        }
        qsfilters = {**self.common_filters, **{
            'activity_type': Reaction.COMMENT,
        }}
        return Reaction.objects.filter(**qsfilters).order_by('-created_at')

    def get(self, request, *args, **kwargs):
        response = super(CommentListByPost, self).get(request, *args, **kwargs)
        gfilters = {**self.common_filters, **{
            'activity_type': Reaction.LIKE,
        }}
        response.data['total_likes'] = Reaction.objects.filter(**gfilters).count()
        
        # check if user logged in and has already liked the status
        if self.request.user.is_anonymous:
            can_like = False
        else:
            user_detail = UserDetail.objects.get(
                auth_user=self.request.user)
            can_like = Reaction.objects.filter(
                **{**gfilters, **{'user': user_detail.id}
                }).count() == 0
        
        response.data['can_like'] = can_like
        return response


class ReactionCreate(generics.CreateAPIView):
    """
        sample payload
        {
          "content_type": "library",
          "object_id": 1,
          "activity_type": "Comment",
          "text": "The first comment by API"
        }
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReactionCreateSerializer
    queryset = Reaction.objects.none()
    allowed_methods = ['POST',]
    
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        try:
            ## add content type id and user details in kwargs
            kwargs['data']['content_type'] = ContentType.objects.get(
                model = kwargs['data']['content_type']).id

            kwargs['data']['user'] = UserDetail.objects.get(
                auth_user=self.request.user).id
        except: pass

        return serializer_class(*args, **kwargs)


class ReactionDelete(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Reaction.objects.all()
    lookup_url_kwarg = 'reaction_id'


class ReactionEdit(generics.UpdateAPIView):
    """
    METHOD : PUT
        {
            "reaction_id": 1
            "text": "updated comment"
        }
    """
    serializer_class =  ReactionEditSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Reaction.objects.all()
    lookup_url_kwarg = 'reaction_id'
    lookup_field = 'pk'
    allowed_methods = ['PUT',]


# TODO Add comment on post (content/library)
# TODO Like/Unlike a post
