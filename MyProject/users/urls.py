from django.urls import path

from .views import *

app_name = 'users'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('thanks-to-you/', view=ReviewThanksView.as_view(), name='review_thanks'),
    
]