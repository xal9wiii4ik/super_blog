from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin

from apps.posts.permissions import IsOwnerOrAuthorizedOrReadOnly, ReadOnly
from apps.posts.serializers import PostModelSerializer, CategoryModelSerializer
from apps.posts.models import Post, Category
from apps.posts.services_views import save_pictures, update_pictures


class PostModelViewSet(ModelViewSet):
    """
    Model view set for model post
    """

    queryset = Post.objects.all()
    serializer_class = PostModelSerializer
    permission_classes = (IsOwnerOrAuthorizedOrReadOnly,)
    parser_classes = (MultiPartParser,)

    def create(self, request, *args, **kwargs):
        response = super(PostModelViewSet, self).create(request, *args, **kwargs)
        if request.FILES:
            save_pictures(files=self.request.FILES.pop('images'), post_id=response.data.get('id'))
        return response

    def partial_update(self, request, *args, **kwargs):
        response = super(PostModelViewSet, self).partial_update(request, *args, **kwargs)
        if request.FILES:
            update_pictures(post_id=response.data['id'], files=request.FILES.pop('images'))
        return response

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
