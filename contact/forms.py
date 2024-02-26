from django import forms
from django.core.exceptions import ValidationError

from contact.models import Contact


class ContactForms(forms.ModelForm):

    # campos presentes no model
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'digite seu nome aqui',
            }
        ),
        label='Nome',
        help_text='apenas o primeiro nome',
        required=True,
        max_length=15,
        min_length=3,
        strip=True
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'digite o restante do seu nome aqui',
            }
        ),
        label='Sobrenome: ',
        help_text='o restante do seu nome',
        required=True,
        max_length=50,
        min_length=3,
        strip=True
    )
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '(+55) 21 98888-7777',
            }
        ),
        label='telefone: ',
        help_text='com o ddd e ddi',
        required=True,
        max_length=13,
        min_length=11,
        strip=True
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'youremail_here@email.com',
            }
        ),
        label='Email: ',
        help_text='seu email',
        required=True,
        max_length=50,
        min_length=3,
    )

    class Meta:
        model = Contact
        fields = (
            'first_name',
            'last_name',
            'phone',
            'email',
            'description',
            'category'
        )

    def clean(self):
        # cleaned_data = self.cleaned_data
        # print(cleaned_data)
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')

        if first_name == last_name:
            msg = ValidationError(
                'O segundo nome não pode ser consoante o primeiro nome',
                code='invalid'
            )
            self.add_error(
                'last_name',
                msg
            )
        return super().clean()

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        validator_name = True
        for letter in str(first_name):
            if letter.isnumeric():
                validator_name = False
                break

        if not validator_name:
            self.add_error(
                'first_name',
                ValidationError(
                    'Não pode conter numeros',
                    code='invalid'
                )
            )

        return first_name
