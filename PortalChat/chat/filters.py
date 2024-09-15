from .models import Response


def filter_user_responses(user_id, title=None, category=None, advertisement_id=None):
    responses = Response.objects.filter(user_id=user_id)

    if title:
        responses = responses.filter(title=title)
    if category:
        responses = responses.filter(category=category)
    if advertisement_id:
        responses = responses.filter(advertisement_id=advertisement_id)

    return responses
