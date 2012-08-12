from django import dispatch

post_created = dispatch.Signal(providing_args=["post_published", "post_location"])