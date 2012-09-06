from django import dispatch

post_created = dispatch.Signal(providing_args=('post', 'request', 'bundle'))
