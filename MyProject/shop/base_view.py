import django.http as http
from django.core.exceptions import PermissionDenied
from django.views import View
from django.shortcuts import render

class BaseView(View):
    """Базовый класс для всех вюшек, который обрабатывает исключения."""
    def dispatch(self, request: http.HttpRequest, *args, **kwargs) -> http.HttpResponse:
        try:
            return super().dispatch(request, *args, **kwargs)
        # Обработка ошыбки 404
        except http.Http404:
            return self.handle_not_found(request, *args, **kwargs)
        
        # Обработка ошыбки 403
        except PermissionDenied:
            return self.handle_forbidden(request, *args, **kwargs)
        
    
    def handle_not_found(self, request, *args, **kwargs):
        context = {'message': 'Ошыбка 404, Страница не найдена'}
        return render(request, 'shop/errors.html', context)
    
    def handle_forbidden(self, request, *args, **kwargs):
        context = {'message': 'Ошыбка 403, у вас не хватает прав.'}
        return render(request, 'shop/errors.html', context)
