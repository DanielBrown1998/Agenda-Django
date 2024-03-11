from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from contact.models import Contact
from django.contrib.auth import password_validation


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
    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
              'accept': 'image/*',
            }
        ),
        label='Imagem '
    )

    class Meta:
        model = Contact
        fields = (
            'first_name',
            'last_name',
            'phone',
            'email',
            'description',
            'category',
            'picture'
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


class RegisterForm(UserCreationForm):

    first_name = forms.CharField(
        widget= forms.TextInput(
            attrs={
                'placeholder': 'seu nome',
            }
        ),
        required=True,
        min_length=3,
        max_length=15,
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'seu sobrenome',
            }
        ),
        required=True,
        min_length=3,
        max_length=100,
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'email@subdominio.com',
            }
        ),
        required=True,
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError(
                    'Esse e-mail já existe',
                    code='invalid'
                )
            )

        return email


class RegisterUpdateForm(forms.ModelForm):

    first_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text="Required.",
        error_messages={
            "min_length": "Please, add more than 2 letters"
        }
    )

    last_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text="Required.",
        error_messages={
            "min_length": "Please, add more than 2 letters"
        }
    )
    password1 = forms.CharField(
        label="Password1",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False
    )
    password2 = forms.CharField(
        label="Password2",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text="Use the same password as before",
        required=False
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)
        password = cleaned_data.get('password1')

        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

    def clean_email(self):

        email = self.cleaned_data.get('email')
        current_email = self.instance.email

        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    ValidationError("Já existe esse email", code='invalid')
                )
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as error:
                self.add_error(
                    'password1',
                    ValidationError(
                        error
                    )
                )

        return password1

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 != password1:
            self.add_error(
                'password2',
                ValidationError(
                    'as senhas são diferentes'
                )
            )

        return super().clean()
