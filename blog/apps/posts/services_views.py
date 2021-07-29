import logging
import os
import typing as tp

from django.contrib.auth import get_user_model
from django.db import models

from apps.posts.models import PostImages, Post, Category
from apps.posts.serializers import PostModelSerializer


def save_pictures(post_id: int, files: tp.List[tp.IO]):
    """ Func for saving pictures in database

    Args:
        post_id: post id
        files: list with files
    """

    for file in files:
        try:
            PostImages.objects.create(post=Post.objects.get(id=post_id),
                                      image=file)
        except Exception:
            logging.exception(msg=f'Something was wrong with creating PostImage for post {post_id}')


def update_pictures(post_id: int, files: tp.List[tp.IO]):
    product_images = PostImages.objects.filter(post__id=post_id)
    for i, file in enumerate(files):
        try:
            product_image = product_images[i]
            os.remove(path=f'images/{product_image.image.name}')
            product_image.image = file
            product_image.save()
        except IndexError:
            pass


def get_posts_filters() -> tp.Dict[str, tp.Any]:
    """
    Get data in the fields without repetitions
    Returns:
        dict with filters
    """

    filters: tp.Dict[tp.Any, tp.Any] = {}
    fields: tp.Dict[str, models.Model] = {
        'name': Category,
        'title': Post,
        'description': Post,
        # todo phrase in description
        'published_date': Post,
        'username': get_user_model(),
    }
    for field in fields:
        try:
            filters.update({field: list(
                fields[field]
                    .objects
                    .order_by()
                    .values(field)
                    .distinct())
            })
        except Exception as e:
            logging.warning(msg=f'Something was wrong {str(e)}')
    return filters


def get_post_fields_by_filters(data: tp.Dict[str, tp.Any]) -> tp.Any:
    """ Getting fields according filters
    Args:
        data: dict with fields for filtering
    Returns:
        dict with stores accordingly, with filtering
    """

    try:
        posts = []
        post_ids: tp.Set[int] = set()
        for key in data.keys():
            ignore_keys = ['published_date']
            values = data[key] if isinstance(data[key], (list, tuple)) and key not in ignore_keys \
                else [data[key]]
            for value in values:
                selector = {key: value}
                intermediate_set = {post.id for post in Post.objects.filter(**selector)}
                post_ids = post_ids.intersection(intermediate_set) if len(post_ids) != 0 else intermediate_set
        for post_id in list(post_ids):
            posts += PostModelSerializer(Post.objects.filter(id=post_id), many=True).data
        return posts
    except Exception as e:
        logging.warning(f'Error in get_fields_by_filters: {str(e)}')
        return {'error': str(e)}
