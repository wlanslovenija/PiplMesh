from django import dispatch

# Signals dispatched when resources are created
post_created = dispatch.Signal(providing_args=('post', 'request', 'bundle'))
comment_created = dispatch.Signal(providing_args=('comment', 'post', 'request', 'bundle'))
