from django.conf.urls import url

from reaction.views import CommentListByPost, ReactionCreate, ReactionEdit, ReactionDelete 

urlpatterns = [
    url(r'^reaction/create/$', ReactionCreate.as_view(), name="comment_like_create"),
    url(r'^reaction/(?P<reaction_id>[-\w]+)/edit/$', ReactionEdit.as_view(), name="comment_edit"),
    url(r'^reaction/(?P<reaction_id>[-\w]+)/delete/$', ReactionDelete.as_view(), name="comment_delete"),
    url(r'^reaction/(?P<post_type>[-\w]+)/(?P<post_id>[-\w]+)/$', CommentListByPost.as_view(), name="comment_list_by_post"),
]
