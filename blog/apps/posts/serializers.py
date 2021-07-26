from rest_framework import serializers

from apps.posts.models import Post, Category, PostImages


class CategoryModelSerializer(serializers.ModelSerializer):
    """
    Model Serializer for model Category
    """

    class Meta:
        model = Category
        fields = '__all__'


class PostImagesModelSerializer(serializers.ModelSerializer):
    """
    Model serializer for model PostImages
    """

    class Meta:
        model = PostImages
        fields = ['id', 'image', 'image_url']

    image_url = serializers.CharField(source='image.url', read_only=True)


class PostModelSerializer(serializers.ModelSerializer):
    """
    Model Serializer for model Post
    """

    class Meta:
        model = Post
        fields = ['id', 'category', 'title', 'description', 'published_date', 'owner', 'post_image']

    post_image = PostImagesModelSerializer(many=True, read_only=True)
