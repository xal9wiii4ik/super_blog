import typing as tp

from django.db import models


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
    image: tp.IO = models.ImageField(verbose_name='image', upload_to='images/', null=True)
    # TODO change upload path

    def __str__(self) -> str:
        return f'pk: {self.pk}, category: {self.category.name}, title: {self.title}'
