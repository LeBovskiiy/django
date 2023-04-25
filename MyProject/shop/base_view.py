import django.http as http
from django.core.exceptions import PermissionDenied
from django.views import View
from django.shortcuts import render, redirect

class BaseView(View):
    """Базовый класс для всех вюшек, который обрабатывает исключения."""
    def dispatch(self, request: http.HttpRequest, *args, **kwargs) -> http.HttpResponse:
        try:
            return super().dispatch(request, *args, **kwargs)
        
        # Обработка ошыбки 404
        except http.Http404 as exception:
            return self.handler404(request, exception, *args, **kwargs)
        
        # Обработка ошыбки 403
        except PermissionDenied as exception:
            return self.handler403(request, exception, *args, **kwargs)
                   
    def handler404(self, request, exception, *args, **kwargs):
        context = {'message': 'Ошибка 404, страница не найдена'}
        return render(request, 'shop/errors.html', context, status=404)
    
    def handler403(self, request, exception, *args, **kwargs):
        context = {'message': 'Ошибка 403, у вас не хватает прав.'}
        return render(request, 'shop/errors.html', context, status=403)
    
    def http_method_not_allowed(request, *args, **kwargs):
        return redirect('method-not-allowed')
    
class MethodNotAllowedView(View):
    def http_method_not_allowed(self, request: http.HttpRequest, *args: any, **kwargs: any) -> http.HttpResponse:
        return render(request, template_name='shop/errors.html', context={'message': 'Ошыбка 405, метод недопустим'}, status=405)