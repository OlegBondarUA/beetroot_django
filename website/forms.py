from django import forms

from . models import Contact


class ContactForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.required:
            self.fields[field].required = True

    class Meta:
        model = Contact
        fields = ('name', 'email', 'message')
        labels = {'name': '', 'email': '', 'message': ''}
        required = ('name', 'email', 'message')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email'}),
            'message': forms.Textarea(
                attrs={
                    'placeholder': 'Your Message',
                    'maxlength': '1000'
                }
            )
        }
