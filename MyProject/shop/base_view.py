from telethon import TelegramClient
import asyncio
import traceback
import functools
import django.http as http
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.views import View

from services.bot import main


class BaseView(View):
    '''Базовый класс для всех вюшек, который обрабатывает исключения.'''
    def dispatch(self, request, *args, **kwargs):
        try:
            response = super().dispatch(request, *args, **kwargs)
        except Exception as e:
            traceback_message = traceback.format_exc()
            asyncio.run(main(str(traceback_message)))

            return http.JsonResponse({'message': str(traceback_message)})
        # Обработка ошыбки 404
        
        except http.Http404 as exception:
            return self.handler404(request, exception, *args, **kwargs)
        
        # Обработка ошыбки 403
        except PermissionDenied as exception:
            return self.handler403(request, exception, *args, **kwargs)
        
        if isinstance(response, (dict, list)):
            return self._response(response)
        else:
            return response
        
    @staticmethod
    def _response(data, *, status=200):
        return http.JsonResponse(
            data,
            status=status,
            safe=not isinstance(data, list)
        )
        
    def handler404(self, request, exception, *args, **kwargs):
        context = {'message': 'Ошибка 404, страница не найдена'}
        return render(request, 'errors.html', context, status=404)
    
    def handler403(self, request, exception, *args, **kwargs):
        context = {'message': 'Ошибка 403, у вас не хватает прав.'}
        return render(request, 'errors.html', context, status=403)
    
    def http_method_not_allowed(request, *args, **kwargs):
        return redirect('method-not-allowed')
    
    
class MethodNotAllowedView(View):
    def http_method_not_allowed(self, request: http.HttpRequest, *args, **kwargs):
        return render(request, template_name='errors.html', context={'message': 'Ошыбка 405, метод недопустим'}, status=405)