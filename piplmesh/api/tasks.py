from __future__ import absolute_import

from celery import task

from . import models

@task.task
def process_notifications_on_new_comment(comment_pk, post_pk):
    post = models.Post.objects.get(pk=post_pk)
    # TODO: https://github.com/wlanslovenija/PiplMesh/issues/299
    comment_pk = int(comment_pk)
    comment = post.comments[comment_pk]

    for subscriber in post.subscribers:
        if subscriber != comment.author:
            models.Notification.objects.create(created_time=comment.created_time, recipient=subscriber, post=post, comment=comment_pk)
