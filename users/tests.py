from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from users.models import User


class UserRegistrationViewTestCase(TestCase):

    def setUp(self) -> None:
        self.data = {
            'username': 'user',
            'email': 'mainuser@yadnex.ru',
            'password1': 'UserPass1234',
            'password2': 'UserPass1234',
        }
        self.path = reverse('users:registration')

    def test_registration_get(self):
        # попытка получить доступ к странице
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/registration.html')
        self.assertContains(response, '<title>Регистрация</title>')

    def test_registration_post_success(self):
        # попытка регистрации нового пользователя
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())

        response = self.client.post(self.path, self.data)
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())

    def test_registration_post_error(self):
        # попытка регистрации нового пользователя с занятым username
        User.objects.create(username=self.data['username'])

        response = self.client.post(self.path, self.data)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.')


class UserLoginViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='user',
            password='UserPass1234'
        )

        self.path = reverse('users:login')
        self.protect_path = reverse('banks:banks')

    def test_login_get(self):
        # проверка правильного шаблона
        response = self.client.get(self.path)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertContains(response, '<title>Авторизация</title>')

    def test_login(self):
        # попытка авторизоваться с верным паролем
        response = self.client.post(self.path, {'username': 'user', 'password': 'UserPass1234'})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('index'))

    def test_login_wrong_password(self):
        # попытка авторизоваться с неверным паролем
        response = self.client.post(self.path, {'username': 'user', 'password': 'UserPass12345'})
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_logout(self):
        # авторизация
        self.client.login(username='user', password='UserPass1234')

        # logout
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_authenticated_access(self):
        # вход в систему
        self.client.login(username='user', password='UserPass1234')

        # проверка доступа к защищенной странице
        response = self.client.get(self.protect_path)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_unauthenticated_access(self):
        # попытка доступа к защищенной странице без аутентификации
        response = self.client.get(self.protect_path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)


class UserProfileViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='user',
            email='mainuser@yadnex.ru',
            password='UserPass1234'
        )
        self.client.login(
            username='user',
            password='UserPass1234'
        )

        self.path = reverse('users:profile', args=[self.user.id])

    def test_profile_get_success(self):
        # проверка на доступность страницы профиля при авторизации
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertContains(response, '<title>Профиль</title>')

    def test_profile_get_error(self):
        # проверка на доступность страницы профиля при отсутствии авторизации
        self.client.logout()
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_profile_update_success(self):
        # успешное обновление профиля
        new_first_name = 'Name'
        new_last_name = 'Lastname'

        response = self.client.post(
            self.path,
            {
                'first_name': new_first_name,
                'last_name': new_last_name,
                'email': self.user.email,
                'username': self.user.username,
            }
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.path)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, new_first_name)
        self.assertEqual(self.user.last_name, new_last_name)

    def test_profile_update_error(self):
        # ошибка в обновление профиля
        new_first_name = 'Name'

        response = self.client.post(
            self.path,
            {
                'first_name': new_first_name,
                'email': self.user.email,
                'username': self.user.username,
            }
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, '')
