from celery import task

from . import models

@task.task
def process_notifications_on_new_comment(comment_pk, post_pk):
    post = models.Post.objects.get(pk=post_pk)
    comment = post.get_comment(comment_pk)

    for subscriber in post.subscribers:
        if subscriber != comment.author:
            models.Notification.objects.create(created_time=comment.created_time, recipient=subscriber, post=post, comment=comment_pk)
