from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin

from apps.posts.serializers import PostModelSerializer, CategoryModelSerializer
from apps.posts.models import Post, Category


class PostModelViewSet(ModelViewSet):
    """
    Model view set for model post
    """

    queryset = Post.objects.all()
    serializer_class = PostModelSerializer


class CategoryViewSet(ListModelMixin,
                      RetrieveModelMixin,
                      GenericViewSet):
    """
    View Set for model category
    """

    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
