from django.contrib.auth.models import AbstractUser
from django.db import models


class Uid(models.Model):
    """
    Model for uid
    """

    class Meta:
        db_table = 'uid'

    uid = models.UUIDField(verbose_name='uuid')
    user_id = models.BigIntegerField(verbose_name='user_id')

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

    image = models.ImageField(verbose_name='image', upload_to='', null=True, blank=True)
    # TODO add optimize images; rename path
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, verbose_name='gender')
    phone = models.CharField(max_length=26, verbose_name='phone')

    def __str__(self) -> str:
        return f'pk: {self.pk}, username: {self.username}, email: {self.email}'
