from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy


from .forms import CustomUserCreationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'


