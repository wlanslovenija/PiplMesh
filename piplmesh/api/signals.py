from django import dispatch

# Signals dispatched when resources are created
post_created = dispatch.Signal(providing_args=('post', 'request', 'bundle'))
comment_created = dispatch.Signal(providing_args=('comment', 'post', 'request', 'bundle'))

# Signals dispatched when resources are updated
post_updated = dispatch.Signal(providing_args=('post', 'request', 'bundle'))
