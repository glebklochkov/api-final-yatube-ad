from django.urls import path, include
from rest_framework import routers

from api import views

router = routers.SimpleRouter()
router.register(r'posts', views.PostViewSet, basename='posts')
router.register(r'posts/(?P<post_id>\d+)/comments', views.CommentViewSet, basename='comments')
router.register(r'groups', views.GroupViewSet, basename='groups')

urlpatterns = [
    path('', include(router.urls)),
    path('follow/', views.FollowViewSet.as_view({
        'get': 'list',
        'post': 'create'
        }),
         name='follow'),
]
