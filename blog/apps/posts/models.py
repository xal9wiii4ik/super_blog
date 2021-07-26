import os
import typing as tp

from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models

from apps.posts.services_models import rename_upload_path, save_picture


class Category(models.Model):
    """
    Table
    """

    class Meta:
        db_table = 'category'

    name: str = models.CharField(max_length=50, verbose_name='name', unique=True)

    def __str__(self) -> str:
        return f'pk: {self.pk}, name: {self.name}'


class Post(models.Model):
    """
    Table for post
    """

    class Meta:
        db_table = 'post'

    category: Category = models.ForeignKey(to=Category,
                                           on_delete=models.SET_NULL,
                                           null=True,
                                           related_name='post_category')
    title: str = models.CharField(max_length=100, verbose_name='title', unique=True)
    description: str = models.TextField(verbose_name='description')
    published_date: datetime = models.DateTimeField(auto_now_add=True, null=True)
    owner: get_user_model() = models.ForeignKey(to=get_user_model(),
                                                on_delete=models.SET_NULL,
                                                null=True,
                                                verbose_name='owner',
                                                related_name='post_owner')

    def __str__(self) -> str:
        return f'pk: {self.pk}, category: {self.category.name}, title: {self.title}'


class PostImages(models.Model):
    """
    Table for image for post
    """

    class Meta:
        db_table = 'post_images'

    image: tp.IO = models.ImageField(verbose_name='image', upload_to='', null=True, blank=True)
    post: Post = models.ForeignKey(to=Post, related_name='post_image', on_delete=models.CASCADE)

    def save(self, *args, **kwargs) -> tp.Any:
        if self.image:
            self.image.name = rename_upload_path(username=self.post.owner.username,
                                                 image_name=self.image.name,
                                                 txt=self.post.title)
        super().save(*args, **kwargs)
        if self.image._file is not None:
            save_picture(image=self.image)

    def delete(self, using=None, keep_parents=False):
        os.remove(path=f'images/{self.image.name}')
        super().delete(using, keep_parents)

    def __str__(self) -> str:
        return f'post_id: {self.post.pk} path: {self.image.name}'
