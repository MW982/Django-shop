from django import forms


class ReviewForm(forms.Form):
    review = forms.CharField(required=True, max_length=500)
