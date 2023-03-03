from django.utils.deprecation import MiddlewareMixin
from zope.dottedname.resolve import resolve

from todolist.todolist import settings



# django2


class DisableCSRF(object):
    """Middleware for disabling CSRF in an specified app name.
    """

    def process_request(self, request):
        """Preprocess the request.
        """
        app_name = "api"
        if resolve(request.path_info).app_name == app_name:
            setattr(request, '_dont_enforce_csrf_checks', True)
        else:
            pass  # check CSRF token validation

# class DisableCSRF(MiddlewareMixin):
#    def process_request(self, request):
#       if settings.DEBUG:
#           setattr(request, '_dont_enforce_csrf_checks', True)
#
#
#
# def simple_middleware(get_response):
#     # Единовременная настройка и инициализация.
#     def middleware(request):
#         # Код должен быть выполнен для каждого запроса
#         # до view
#         response = get_response(request)
#         # Код должен быть выполнен ответа после view
#         return response
#     return middleware