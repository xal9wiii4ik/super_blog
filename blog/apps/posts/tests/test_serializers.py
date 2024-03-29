from django.db.models import F
from django.test import TestCase

from apps.posts.models import Post, Category
from apps.posts.serializers import CategoryModelSerializer, PostModelSerializer


class SerializerTestCase(TestCase):
    """
    Test for serializers
    """

    def setUp(self) -> None:
        self.category = Category.objects.create(name='category')
        self.category_1 = Category.objects.create(name='category_1')
        self.post = Post.objects.create(title='first title for posts',
                                        description='description for first post',
                                        category=self.category_1)
        self.post_1 = Post.objects.create(title='this is the second title for posts',
                                          description='this is description for second post',
                                          category=self.category)

    def test_category_serializer(self) -> None:
        """
        Test for serializer of category
        """

        categories = Category.objects.all()
        data = CategoryModelSerializer(categories, many=True).data

        expected_data = [
            {
                'id': self.category.pk,
                'name': 'category'
            },
            {
                'id': self.category_1.pk,
                'name': 'category_1'
            }
        ]
        self.assertEqual(expected_data, data)

    def test_post_serializer(self) -> None:
        """
        Test for serializer of category
        """

        posts = Post.objects.all()
        data = PostModelSerializer(posts, many=True).data

        expected_data = [
            {
                'id': self.post.pk,
                'title': 'first title for posts',
                'description': 'description for first post',
                'image': None,
                'published_date': self.post.published_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'category': self.category_1.pk,
                'owner': None,
            },
            {
                'id': self.post_1.pk,
                'title': 'this is the second title for posts',
                'description': 'this is description for second post',
                'image': None,
                'published_date': self.post_1.published_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'category': self.category.pk,
                'owner': None,
            }
        ]
        self.assertEqual(first=data, second=expected_data)
