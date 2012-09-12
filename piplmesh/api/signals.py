from django import dispatch

post_created = dispatch.Signal(providing_args=('post', 'request', 'bundle'))
post_updated = dispatch.Signal(providing_args=('post', 'request', 'bundle'))
