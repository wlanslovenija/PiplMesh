from django.utils.translation import ugettext_lazy as _

from mongo_auth import backends

from piplmesh import panels

class OnlineUsersPanel(panels.BasePanel):
    def get_context(self, context):
        context = super(OnlineUsersPanel, self).get_context(context)

        context.update({
            'header': _("Online users"),
            'online_users': backends.User.objects(is_online=True),
        })
        return context

panels.panels_pool.register(OnlineUsersPanel)
