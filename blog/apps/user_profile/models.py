from django.contrib.auth.models import AbstractUser
from django.db import models


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
