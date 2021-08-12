import typing as tp

from celery import shared_task

from apps.user_profile.tasks.tasks import send_telegram_message


@shared_task
def mail_posts_to_subscribers(post_data: tp.Dict[str, tp.Union[int, str]],
                              owner_id: int,
                              files: tp.Optional[tp.List[tp.Any]]) -> None:
    """ Mail new posts to subscribers
    Args:
        post_data: dict with information about new post
        owner_id: id of owner
        files: list with files
    """

    from django.contrib.auth import get_user_model

    user = get_user_model().objects.get(id=owner_id)
    for subscriber in user.subscribers_owner.subscribers.all():
        if subscriber.telegram_chat_id is not None:
            send_telegram_message.delay(
                chat_id=subscriber.telegram_chat_id,
                message=f'{user.username} posted a new post, rather look at it)\n'
                        f'Tittle: {post_data["title"]}\n'
                        f'Description: {post_data["description"][:20]}...\n'
                        f'link:',
                files=files)
            # TODO add link to new post(after updated vue.js)
