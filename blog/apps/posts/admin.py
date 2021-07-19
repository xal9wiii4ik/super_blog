import inspect
import sys

from django.contrib import admin
from django.db.models.base import ModelBase

for _, cls in inspect.getmembers(sys.modules['apps.posts.models']):
    if isinstance(cls, ModelBase):
        admin.site.register(cls)

