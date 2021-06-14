from rest_framework.serializers import ModelSerializer

from apps.posts.models import Post, Category


class CategoryModelSerializer(ModelSerializer):
    """
    Model Serializer for model Category
    """

    class Meta:
        model = Category
        fields = '__all__'


class PostModelSerializer(ModelSerializer):
    """ Model Serializer for model Post """

    class Meta:
        model = Post
        fields = '__all__'
