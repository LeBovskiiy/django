from django import forms

from users.models import UserReview


class UserReviewForm(forms.ModelForm):
    class Meta:
        model = UserReview
        fields = ('rate', 'comment',)
