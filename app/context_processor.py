from django.http import HttpRequest


def url_navigation(request: HttpRequest):
    url = request.resolver_match
    url_name = None
    target = None

    if url:
        url_name = url.url_name
        target = url.app_name

    context = {
        'current_url': request.path,
        'url_name': url_name,
        'target': target,
    }

    return context
