import typing as tp
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.posts.models import save_picture


class Uid(models.Model):
    """
    Model for uid
    """

    class Meta:
        db_table = 'uid'

    uid = models.UUIDField(verbose_name='uuid')
    user_id = models.BigIntegerField(verbose_name='user_id')
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
    # TODO add optimize images; rename path
    gender: str = models.CharField(max_length=6, choices=GENDER_CHOICES, verbose_name='gender')
    phone: str = models.CharField(max_length=26, verbose_name='phone')

    def save(self, *args, **kwargs) -> tp.Any:
        super().save(*args, **kwargs)
        if self.image._file is not None:
            print(1)
            save_picture(image=self.image)

    def __str__(self) -> str:
        return f'pk: {self.pk}, username: {self.username}, email: {self.email}'
