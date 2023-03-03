from django.utils.deprecation import MiddlewareMixin

from todolist.todolist import settings


class DisableCSRF(MiddlewareMixin):
   def process_request(self, request):
      if settings.DEBUG:
          setattr(request, '_dont_enforce_csrf_checks', True)



def simple_middleware(get_response):
    # Единовременная настройка и инициализация.
    def middleware(request):
        # Код должен быть выполнен для каждого запроса
        # до view
        response = get_response(request)
        # Код должен быть выполнен ответа после view
        return response
    return middleware