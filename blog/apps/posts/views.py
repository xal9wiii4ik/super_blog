from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin

from apps.posts.permissions import IsOwnerOrAuthorizedOrReadOnly, ReadOnly
from apps.posts.serializers import PostModelSerializer, CategoryModelSerializer
from apps.posts.models import Post, Category
from apps.posts.services_views import save_pictures, update_pictures, get_posts_filters, get_post_fields_by_filters
from apps.posts.tasks.tasks import mail_posts_to_subscribers


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
        files = []
        if request.FILES:
            files = self.request.FILES.pop('images')
            save_pictures(files=files, post_id=response.data.get('id'))
        if len(request.user.subscribers_owner.subscribers.all()) > 0:
            mail_posts_to_subscribers.delay(
                post_data=response.data,
                owner_id=request.user.id,
                files=files if len(files) > 0 else None)
        return response

    def partial_update(self, request, *args, **kwargs):
        response = super(PostModelViewSet, self).partial_update(request, *args, **kwargs)
        if request.FILES:
            update_pictures(post_id=response.data['id'], files=request.FILES.pop('images'))
        return response

    def perform_create(self, serializer) -> None:
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class PostFilters(APIView):
    """
    View for post filters
    """

    def get(self, request: Request) -> Response:
        data = get_posts_filters()
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        data = get_post_fields_by_filters(data=request.data)
        data = {'none': 'No posts were found for the specified filters'} if len(data) == 0 else data
        return Response(data=data, status=status.HTTP_200_OK)


class CategoryViewSet(ListModelMixin,
                      RetrieveModelMixin,
                      GenericViewSet):
    """
    View Set for model category
    """

    permission_classes = (ReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
