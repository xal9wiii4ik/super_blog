import json

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.posts.models import Post, Category
from apps.posts.serializers import PostModelSerializer, CategoryModelSerializer


class CategoryApiTestCase(APITestCase):
    """
    Api test for categories
    """

    def setUp(self) -> None:
        self.category = Category.objects.create(name='category')
        self.category_1 = Category.objects.create(name='category_1')

    def test_get(self) -> None:
        """
        Get categories
        """

        url = reverse('post:category-list')
        categories = Category.objects.all()
        response = self.client.get(path=url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(CategoryModelSerializer(categories, many=True).data,
                         response.data)

    def test_get_retrieve(self) -> None:
        """
        Get one category
        """

        url = reverse('post:category-detail', args=(self.category.pk,))
        response = self.client.get(path=url)
        self.assertEqual(first=status.HTTP_200_OK, second=response.status_code)
        self.assertEqual(CategoryModelSerializer(self.category).data,
                         response.data)

    def test_create(self) -> None:
        """
        Create new category
        """

        url = reverse('post:category-list')
        data = {
            'name': 'something new'
        }
        json_data = json.dumps(data)
        response = self.client.post(path=url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(first=status.HTTP_405_METHOD_NOT_ALLOWED, second=response.status_code)

    def test_delete(self) -> None:
        """
        Delete category
        """

        url = reverse('post:category-detail', args=(self.category.pk,))
        response = self.client.delete(path=url)
        self.assertEqual(first=status.HTTP_405_METHOD_NOT_ALLOWED, second=response.status_code)

    def test_update(self) -> None:
        """
        Update category
        """

        url = reverse('post:category-detail', args=(self.category.pk,))
        data = {
            'name': 'new name'
        }
        json_data = json.dumps(data)
        response = self.client.put(path=url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(first=status.HTTP_405_METHOD_NOT_ALLOWED, second=response.status_code)


class PostApiTestCase(APITestCase):
    """
    Api test for post
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

    def test_get(self) -> None:
        """
        Get posts
        """

        url = reverse('post:post-list')
        categories = Post.objects.all()
        response = self.client.get(path=url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(PostModelSerializer(categories, many=True).data,
                         response.data)

    def test_get_retrieve(self) -> None:
        """
        Get one post
        """

        url = reverse('post:post-detail', args=(self.post.pk,))
        response = self.client.get(path=url)
        self.assertEqual(first=status.HTTP_200_OK, second=response.status_code)
        self.assertEqual(PostModelSerializer(self.post).data,
                         response.data)

    def test_create(self) -> None:
        """
        Create new post
        """

        self.assertEqual(first=Post.objects.all().count(), second=2)
        url = reverse('post:post-list')
        data = {
            'title': 'title',
            'description': 'description',
            'category': self.category.pk
        }
        json_data = json.dumps(data)
        response = self.client.post(path=url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(first=status.HTTP_201_CREATED, second=response.status_code)
        self.assertEqual(first=Post.objects.all().count(), second=3)

    def test_delete(self) -> None:
        """
        Delete post
        """

        self.assertEqual(first=Post.objects.all().count(), second=2)
        url = reverse('post:post-detail', args=(self.post.pk,))
        response = self.client.delete(path=url)
        self.assertEqual(first=status.HTTP_204_NO_CONTENT, second=response.status_code)
        self.assertEqual(first=Post.objects.all().count(), second=1)

    def test_update(self) -> None:
        """
        Update post
        """

        self.assertEqual(first=self.post.title, second='first title for posts')
        url = reverse('post:post-detail', args=(self.post.pk,))
        data = {
            'title': 'new title'
        }
        json_data = json.dumps(data)
        response = self.client.patch(path=url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(first=status.HTTP_200_OK, second=response.status_code)
        self.post.refresh_from_db()
        self.assertEqual(first=self.post.title, second='new title')
