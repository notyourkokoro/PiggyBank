from django.forms import CharField, EmailInput, TextInput, PasswordInput, ImageField, FileInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm

from users.models import User


class UserRegistrationForm(UserCreationForm):
    username = CharField(
        widget=TextInput(
            attrs={
                'class': 'form-control form-control-lg'
            }
        )
    )

    email = CharField(
        widget=EmailInput(
            attrs={
                'class': 'form-control form-control-lg'
            }
        )
    )

    password1 = CharField(
        widget=PasswordInput(
            attrs={
                'class': 'form-control form-control-lg'
            }
        )
    )

    password2 = CharField(
        widget=PasswordInput(
            attrs={
                'class': 'form-control form-control-lg'
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    # подумать насчет отправки email для подтверждения почты
    # def save(self, commit=True) -> User:
    #     user = super(UserRegistrationForm, self).save(commit=commit)
    #     return user


class UserLoginForm(AuthenticationForm):
    username = CharField(
        widget=TextInput(
            attrs={
                'class': 'form-control form-control-lg'
            }
        )
    )

    password = CharField(
        widget=PasswordInput(
            attrs={
                'class': 'form-control form-control-lg'
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'password')


class UserProfileForm(UserChangeForm):
    first_name = CharField(
        widget=TextInput(
            attrs={
                'class': 'form-control form-control-lg'
            }
        )
    )

    last_name = CharField(
        widget=TextInput(
            attrs={
                'class': 'form-control form-control-lg'
            }
        )
    )

    username = CharField(
        widget=TextInput(
            attrs={
                'class': 'form-control form-control-lg',
                'readonly': True
            }
        )
    )

    email = CharField(
        widget=EmailInput(
            attrs={
                'class': 'form-control form-control-lg',
                'readonly': True
            }
        )
    )

    img = ImageField(
        widget=FileInput(
            attrs={
                'class': 'form-control form-control-lg'
            }
        ),
        required=False
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'img')
