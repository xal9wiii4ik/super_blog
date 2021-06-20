import typing as tp
import os

from PIL import Image
from datetime import datetime

from django.db import models

SIZE = (800, 768)


def save_picture(image: tp.IO):
    img = Image.open(image)
    name = image.name
    format = name.split('.')[-1]
    # TODO format
    if (img.size[0] < SIZE[0]) or (img.size[-1] < SIZE[-1]):
        # TODO exception
        raise Exception('size')
    else:
        os.remove(path=f'images/{name}')
        # TODO rename
        img.save(f'images/{name}', format=format, quality=50)


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
    title: str = models.CharField(max_length=100, verbose_name='title')
    description: str = models.TextField(verbose_name='description')
    image: tp.IO = models.ImageField(verbose_name='image', upload_to='', null=True, blank=True)
    published_date: datetime = models.DateTimeField(auto_now_add=True, null=True)

    # TODO change upload path
    # image: quality: 50; size: (800, 768);

    def save(self, *args, **kwargs) -> tp.Any:
        super().save(*args, **kwargs)
        if self.image._file is not None:
            print(1)
            save_picture(image=self.image)

    def __str__(self) -> str:
        return f'pk: {self.pk}, category: {self.category.name}, title: {self.title}'
