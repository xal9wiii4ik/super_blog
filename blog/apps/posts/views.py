from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin

from apps.posts.permissions import IsOwnerOrReadOnly, ReadOnly
from apps.posts.serializers import PostModelSerializer, CategoryModelSerializer
from apps.posts.models import Post, Category


class PostModelViewSet(ModelViewSet):
    """
    Model view set for model post
    """

    queryset = Post.objects.all()
    serializer_class = PostModelSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    parser_classes = (MultiPartParser,)

    def perform_create(self, serializer) -> None:
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class CategoryViewSet(ListModelMixin,
                      RetrieveModelMixin,
                      GenericViewSet):
    """
    View Set for model category
    """

    permission_classes = (ReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
