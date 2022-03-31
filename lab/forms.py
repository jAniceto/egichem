from django import forms
from website.models import Member


class SendEmailForm(forms.Form):
    email_to = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'checked': ''}), 
        queryset=Member.objects.filter(alumni=False).order_by('name'), 
        required=True,
    )
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
