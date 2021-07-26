import logging
import os
import typing as tp

from apps.posts.models import PostImages, Post


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
