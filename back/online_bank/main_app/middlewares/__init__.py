from utils import UserContext


class ContextMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        response = self._get_response(request)
        UserContext.drop_user()
        return response
