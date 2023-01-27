from rest_framework.routers import SimpleRouter
from django.urls import include, path

from api.views import PostViewSet, GroupViewSet, CommentViewSet, FollowViewSet

router = SimpleRouter()
router.register(r'v1/posts', PostViewSet)
router.register(r'v1/groups', GroupViewSet)
router.register(r'v1/follow', FollowViewSet, basename='follow')
router.register(
    r'v1/posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comments'
)
urlpatterns = [
    path('v1/', include('djoser.urls.jwt')),
    path('', include(router.urls)),
]
