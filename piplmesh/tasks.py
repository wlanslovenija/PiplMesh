from celery.task import task

from pushserver.utils import updates

from piplmesh.account import models

@task
def prune_users():
    print "tasks add"
    
    chan_users = models.User.objects()
    for user in chan_users:
        cl = user.clist
        dl = user.dlist
        print cl
        print dl
        for el in dl:
            try:
                cl.remove(el)
            except ValueError:
                pass
        print len(cl)

        if len(cl) == 0 and len(dl) > 0:
            channel_id = 'a'
            for el in dl:
                user.update(pull__clist=el)
                user.update(pull__dlist=el)
            user.update(set__logged=False)
            updates.send_update(channel_id, {'type':'answer', 'value':{'action':'PART', 'message':user.username}})
    return x + y