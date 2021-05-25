from functools import wraps

from utils.response import UnauthorizedJsonResponse


def login_required(view_func):

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return UnauthorizedJsonResponse()
        return view_func(request, *args, **kwargs)

    return _wrapped_view