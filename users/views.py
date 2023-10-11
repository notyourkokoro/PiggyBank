from django.urls import reverse_lazy

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView

from django.contrib.messages.views import SuccessMessageMixin

from common.mixins import TitleMixin
from users.models import User
from users.forms import UserRegistrationForm, UserLoginForm, UserProfileForm


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Теперь Вы с нами!'

    title = 'Регистрация'


class UserLoginView(TitleMixin, SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    title = 'Авторизация'


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    title = 'Профиль'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


class DeleteUserView(SuccessMessageMixin, DeleteView):
    model = User
    success_url = reverse_lazy('users:login')
    success_message = 'Аккаунт был успешно удален!'
