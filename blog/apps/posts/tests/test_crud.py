import json

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
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
        password = make_password('password')
        url = reverse('token')

        self.user = get_user_model().objects.create(username='first user',
                                                    password=password,
                                                    gender='male',
                                                    phone='12312321',
                                                    email='check@yandex.ru',
                                                    is_active=True,
                                                    is_superuser=True,
                                                    is_staff=True)
        data = {
            'username': self.user.username,
            'password': 'password'
        }
        json_data = json.dumps(data)
        self.token = f"Token " \
                     f"{self.client.post(path=url, data=json_data, content_type='application/json').data['access']}"

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
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(path=url, data=json_data,
                                    content_type='application/json')
        self.assertEqual(first=status.HTTP_403_FORBIDDEN, second=response.status_code)

    def test_delete(self) -> None:
        """
        Delete category
        """

        url = reverse('post:category-detail', args=(self.category.pk,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.delete(path=url)
        self.assertEqual(first=status.HTTP_403_FORBIDDEN, second=response.status_code)

    def test_update(self) -> None:
        """
        Update category
        """

        url = reverse('post:category-detail', args=(self.category.pk,))
        data = {
            'name': 'new name'
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.put(path=url, data=json_data,
                                   content_type='application/json')
        self.assertEqual(first=status.HTTP_403_FORBIDDEN, second=response.status_code)


class PostApiTestCase(APITestCase):
    """
    Api test for post
    """

    def setUp(self) -> None:
        password = make_password('password')
        url = reverse('token')

        self.user = get_user_model().objects.create(username='first user',
                                                    password=password,
                                                    gender='male',
                                                    phone='12312321',
                                                    email='check@yandex.ru',
                                                    is_active=True)
        data = {
            'username': self.user.username,
            'password': 'password'
        }
        json_data = json.dumps(data)
        self.token = f"Token " \
                     f"{self.client.post(path=url, data=json_data, content_type='application/json').data['access']}"

        self.user_1 = get_user_model().objects.create(username='second user',
                                                      password=password,
                                                      gender='female',
                                                      phone='87878127',
                                                      is_active=True)
        data_1 = {
            'username': self.user_1.username,
            'password': 'password'
        }
        json_data_1 = json.dumps(data_1)
        self.token_1 = f"Token " \
                       f"{self.client.post(path=url, data=json_data_1, content_type='application/json').data['access']}"
        self.category = Category.objects.create(name='category')
        self.category_1 = Category.objects.create(name='category_1')

        self.post = Post.objects.create(title='first title for posts',
                                        description='description for first post',
                                        category=self.category_1,
                                        owner=self.user)
        self.post_1 = Post.objects.create(title='this is the second title for posts',
                                          description='this is description for second post',
                                          category=self.category,
                                          owner=self.user_1)

    def test_get(self) -> None:
        """
        Get posts
        """

        url = reverse('post:post-list')
        categories = Post.objects.all()
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
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
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(path=url, data=data, format='multipart')
        self.assertEqual(first=status.HTTP_201_CREATED, second=response.status_code)
        self.assertEqual(first=Post.objects.all().count(), second=3)

    def test_create_un_authorize(self) -> None:
        """
        Create new post un authorize
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
        self.assertEqual(first=status.HTTP_401_UNAUTHORIZED, second=response.status_code)
        self.assertEqual(first=Post.objects.all().count(), second=2)

    def test_delete(self) -> None:
        """
        Delete post
        """

        self.assertEqual(first=Post.objects.all().count(), second=2)
        url = reverse('post:post-detail', args=(self.post.pk,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.delete(path=url)
        self.assertEqual(first=status.HTTP_204_NO_CONTENT, second=response.status_code)
        self.assertEqual(first=Post.objects.all().count(), second=1)

    def test_delete_un_authorize(self) -> None:
        """
        Delete post un authorize
        """

        self.assertEqual(first=Post.objects.all().count(), second=2)
        url = reverse('post:post-detail', args=(self.post.pk,))
        response = self.client.delete(path=url)
        self.assertEqual(first=status.HTTP_401_UNAUTHORIZED, second=response.status_code)
        self.assertEqual(first=Post.objects.all().count(), second=2)

    def test_delete_not_owner(self) -> None:
        """
        Delete post not owner
        """

        self.assertEqual(first=Post.objects.all().count(), second=2)
        url = reverse('post:post-detail', args=(self.post.pk,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.delete(path=url)
        self.assertEqual(first=status.HTTP_403_FORBIDDEN, second=response.status_code)
        self.assertEqual(first=Post.objects.all().count(), second=2)

    def test_update(self) -> None:
        """
        Update post
        """

        self.assertEqual(first=self.post.title, second='first title for posts')
        url = reverse('post:post-detail', args=(self.post.pk,))
        data = {
            'title': 'new title'
        }
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.patch(path=url, data=data, format='multipart')
        self.assertEqual(first=status.HTTP_200_OK, second=response.status_code)
        self.post.refresh_from_db()
        self.assertEqual(first=self.post.title, second='new title')

    def test_update_un_authorize(self) -> None:
        """
        Update post un authorize
        """

        self.assertEqual(first=self.post.title, second='first title for posts')
        url = reverse('post:post-detail', args=(self.post.pk,))
        data = {
            'title': 'new title'
        }
        json_data = json.dumps(data)
        response = self.client.patch(path=url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(first=status.HTTP_401_UNAUTHORIZED, second=response.status_code)

    def test_update_not_owner(self) -> None:
        """
        Update post not owner
        """

        self.assertEqual(first=self.post.title, second='first title for posts')
        url = reverse('post:post-detail', args=(self.post.pk,))
        data = {
            'title': 'new title'
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.patch(path=url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(first=status.HTTP_403_FORBIDDEN, second=response.status_code)
        self.post.refresh_from_db()
        self.assertEqual(first=self.post.title, second='first title for posts')
