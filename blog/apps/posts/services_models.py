import os
import typing as tp

from PIL import Image

from django.utils import timezone

SIZE = (800, 768)


def rename_upload_path(image_name: str, username: str, txt: str) -> str:
    """ Rename upload path of image(set unique)

    Args:
        image_name: image name
        username: username
        txt: unique field
    Returns:
        new image name
    """

    time = timezone.now().strftime("%d-%m-%Y-%H-%S")
    image_extension = image_name.split('.')[-1]
    rename = username + '/' + str(txt) + ':' + time + '.' + image_extension
    return os.path.join(rename)


def save_picture(image: tp.IO):
    """ Optimize picture

    Args:
        image: image
    """

    img = Image.open(image)
    name = image.name
    format = name.split('.')[-1]
    if (img.size[0] < SIZE[0]) or (img.size[-1] < SIZE[-1]):
        raise Exception('Bad size (models.Model)')
    else:
        os.remove(path=f'images/{name}')
        img.save(f'images/{name}', format=format, quality=50)