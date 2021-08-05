import os
import typing as tp

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.posts.services_models import rename_upload_path, save_picture


class Uid(models.Model):
    """
    Model for uid
    """

    class Meta:
        db_table = 'uid'

    uid = models.UUIDField(verbose_name='uuid')
    user_id = models.BigIntegerField(verbose_name='user_id')
    updated_data = models.CharField(max_length=200, verbose_name='updated_data', null=True)
    date_created = models.DateField(verbose_name='date_created', auto_now_add=True)

    def __str__(self) -> str:
        return f'pk: {self.pk}, uid: {self.uid}, user_id: {self.user_id}'


class Account(AbstractUser):
    """
     Model for user account
    """

    class Meta:
        db_table = 'account'
        abstract = False

    GENDER_CHOICES = [
        ('male', 'male'),
        ('female', 'female')
    ]

    image: tp.IO = models.ImageField(verbose_name='image', upload_to='', null=True, blank=True)
    gender: str = models.CharField(max_length=6, choices=GENDER_CHOICES, verbose_name='gender')
    phone: str = models.CharField(max_length=26, verbose_name='phone')
    telegram_chat_id: str = models.CharField(max_length=50,
                                             verbose_name='telegram chat id',
                                             unique=True,
                                             null=True,
                                             blank=True)

    def save(self, *args, **kwargs) -> tp.Any:
        if self.image:
            self.image.name = rename_upload_path(username=self.username,
                                                 image_name=self.image.name,
                                                 txt=self.email)
        super().save(*args, **kwargs)
        if self.image._file is not None:
            save_picture(image=self.image)

    def delete(self, using=None, keep_parents=False):
        os.remove(path=f'images/{self.image.name}')
        super().delete(using, keep_parents)

    def __str__(self) -> str:
        return f'pk: {self.pk}, username: {self.username}, email: {self.email} path: {self.image.name}'


class TelegramGroup(models.Model):
    """
    Model for telegram group(logging)
    """

    class Meta:
        db_table = 'telegram_group'

    group_id: str = models.CharField(max_length=50, verbose_name='telegram group id')
    group_type: str = models.CharField(max_length=10, verbose_name='type of telegram group')
    users: tp.List[get_user_model()] = models.ManyToManyField(to=get_user_model(),
                                                              related_name='user_telegram_group')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'id: {self.pk}, group_id: {self.group_id}'


class UserSubscriber(models.Model):
    """
    Model for user subscriber
    """

    class Meta:
        db_table = 'user_subscriber'

    owner: get_user_model() = models.OneToOneField(to=get_user_model(),
                                                   on_delete=models.CASCADE,
                                                   related_name='subscribers_owner')
    subscribers: tp.List[get_user_model()] = models.ManyToManyField(to=get_user_model(),
                                                                    related_name='subscriber_users',
                                                                    blank=True)

    def __str__(self) -> str:
        #         TODO check list subscribers to str
        return f'id: {self.pk}'
