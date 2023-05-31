from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, TemplateView,
                                  UpdateView, View)

from .forms import CustomUserCreationForm
from .models import CustomUser, UserReview


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'


class ReviewThanksView(View):

    def get(self, request):
        context = {
            'username': request.user,
            'text': f'{request.user} Thanks for your feedback'
        }
        return render(request, 'users/review_thanks.html', context)
