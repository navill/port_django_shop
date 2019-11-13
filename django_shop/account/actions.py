from django.contrib.contenttypes.models import ContentType

from account.models import Action


def track_action(user, verb, content_object=None):
    action = Action(user=user, verb=verb, content_object=content_object)
    action.save()
    return True
