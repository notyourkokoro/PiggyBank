from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from banks.models import Bank
from users.models import User


class IndexViewTestCase(TestCase):

    def setUp(self):
        self.path = reverse('index')

    def test_index_get(self):
        # получение запроса
        response = self.client.get(self.path)

        # проверка на соответствие получаемых данных в get-запросе
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'banks/index.html')
        self.assertContains(response, '<title>Главная</title>')


class BanksViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='user',
            password='UserPass1234'
        )
        self.client.login(
            username='user',
            password='UserPass1234'
        )

        self.bank = Bank.objects.create(
            name='Test Bank',
            goal='100',
            owner=self.user
        )

        self.path = reverse('banks:banks')

    def test_banks_get_success(self):
        # получение запроса
        response = self.client.get(self.path)

        # проверка на соответствие получаемых данных в get-запросе
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'banks/banks.html')
        self.assertContains(response, 'Копилки')

    def test_banks_get_error(self):
        # попытка получить доступ к странице без авторизации
        self.client.logout()
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_add_money_success(self):
        data = {
            'bank_id': self.bank.pk,
            'money': 30,
        }

        # получение запроса
        response = self.client.post(self.path, data)

        # проверка обновления данных
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('banks:banks'))

        self.bank.refresh_from_db()
        self.assertEqual(self.bank.current, 30)

    def test_add_money_error(self):
        data = {
            'bank_id': self.bank.pk,
            'money': 250,
        }

        # получение запроса
        response = self.client.post(self.path, data)

        # проверка, что данные не были обновлены
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(response, 'form', 'money', 'В копилке не может содержаться денег больше, чем цель!')

        self.bank.refresh_from_db()
        self.assertEqual(self.bank.current, 0)


class DeleteBankViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='user',
            password='UserPass1234'
        )
        self.client.login(
            username='user',
            password='UserPass1234'
        )

        self.bank = Bank.objects.create(
            name='Test Bank',
            goal='100',
            owner=self.user
        )

        self.path = reverse('banks:delete_bank', args=[self.bank.pk])

    def test_delete_bank_success(self):
        # получение запроса
        response = self.client.post(self.path)

        # проверка на соответствие получаемых данных в get-запросе
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('banks:banks'))
        self.assertFalse(Bank.objects.filter(pk=self.bank.pk).exists())

    def test_delete_bank_error(self):
        # попытка получить доступ к странице без авторизации
        self.client.logout()
        response = self.client.post(self.path)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        # проверка, что банк не был удален
        self.assertTrue(Bank.objects.filter(pk=self.bank.pk).exists())


class ExitBankViewTestCase(TestCase):

    def setUp(self):
        self.main_user = User.objects.create_user(
            username='user',
            password='UserPass1234'
        )
        self.client.login(
            username='user',
            password='UserPass1234'
        )

        self.another_user = User.objects.create_user(
            username='another_user',
            password='UserPass1234'
        )

        self.bank = Bank.objects.create(
            name='Test Bank',
            goal='100',
            owner=self.another_user
        )
        self.bank.users.add(self.main_user)

        self.path = reverse('banks:exit_bank', args=[self.bank.pk])

    def test_exit_bank_success(self):
        # получение запроса
        response = self.client.post(self.path)

        # проверка на соответствие получаемых данных в get-запросе
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('banks:banks'))
        self.assertFalse(self.bank.users.filter(username='user').exists())

    def test_exit_bank_error(self):
        # попытка получить доступ к странице без авторизации
        self.client.logout()
        response = self.client.post(self.path)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        # проверка, что пользователь все еще находится в копилке
        self.assertTrue(self.bank.users.filter(username='user').exists())


class CreateBanksViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='user',
            password='UserPass1234'
        )
        self.client.login(
            username='user',
            password='UserPass1234'
        )

        self.data_success = {
            'name': 'Test Bank',
            'goal': 100,
            'currency': 'USD'
        }

        self.data_error = {
            'name': 'Test Bank',
            'goal': 100,
        }

        self.path = reverse('banks:create_bank')

    def test_create_bank_get_success(self):
        # получение запроса
        response = self.client.get(self.path)

        # проверка на соответствие получаемых данных в get-запросе
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'banks/create_bank.html')
        self.assertContains(response, '<title>Создать копилку</title>')

    def test_create_bank_get_error(self):
        # попытка получить доступ к странице без авторизации
        self.client.logout()
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.FOUND)

    def test_create_bank_post_success(self):
        # получение запроса на создание копилки
        response = self.client.post(self.path, self.data_success)

        # проверка, что запрос выполнился успешно
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('banks:banks'))

        self.user.refresh_from_db()
        self.assertTrue(Bank.objects.filter(name='Test Bank').exists())
        bank = Bank.objects.get(name='Test Bank')
        self.assertEqual(bank.owner, self.user)

    def test_create_bank_post_error(self):
        # получение запроса с отправкой данных о создании копилки с некорректными данными
        response = self.client.post(self.path, self.data_error)

        # проверка, что копилка не была создана
        self.assertEquals(response.status_code, HTTPStatus.OK)

        self.user.refresh_from_db()
        self.assertFalse(Bank.objects.filter(name='Test Bank').exists())
        self.assertFalse(self.user.banks.filter(name='Test Bank').exists())


class EditBankViewTestCase(TestCase):

    def setUp(self):
        self.main_user = User.objects.create_user(
            username='user',
            password='UserPass1234'
        )
        self.client.login(
            username='user',
            password='UserPass1234'
        )

        self.another_user = User.objects.create_user(
            username='AnotherUser',
            password='UserPass1234'
        )

        self.data = {
            'name': 'Test Bank',
            'goal': 100,
            'currency': 'USD'
        }

        self.bank = Bank.objects.create(
            **self.data,
            current=99,
            owner=self.main_user,
        )

        self.data_success = {
            'name': 'New Test Bank',
            'description': 'New test description',
            'goal': 250,
            'currency': 'EUR',
        }

        self.data_error = {
            'goal': 95,
        }

        self.path = reverse('banks:edit_bank', args=[self.bank.pk])

    def test_edit_bank_get_success(self):
        # получение запроса
        response = self.client.get(self.path)

        # проверка на соответствие получаемых данных в get-запросе
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'banks/bank_profile.html')
        self.assertContains(response, '<title>Редактировать копилку</title>')

    def test_edit_bank_get_error(self):
        # попытка получить доступ к странице без авторизации
        self.client.logout()
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.FOUND)

    def test_edit_bank_post_success(self):
        # получение запроса
        response = self.client.post(self.path, self.data_success)

        # проверка изменений в копилке, что они были успешно применены
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.path)

        self.bank.refresh_from_db()
        self.assertEqual(self.bank.name, 'New Test Bank')
        self.assertEqual(self.bank.description, 'New test description')
        self.assertEqual(self.bank.goal, 250.00)
        self.assertEqual(self.bank.currency, 'EUR')

    def test_edit_bank_post_error(self):
        # получение запроса с попыткой установить значение цели меньше текущих накоплений
        response = self.client.post(self.path, self.data_error)

        # проверка, что формы вывод ошибку и не применяет изменения
        self.assertFormError(response, 'form', 'goal', 'Текущие накопления не могут превышать новую цель!')

        self.assertEquals(response.status_code, HTTPStatus.OK)

        self.bank.refresh_from_db()
        self.assertEqual(self.bank.goal, 100)

    def test_edit_bank_post_add_user_success(self):
        data = self.data
        data['new_user'] = self.another_user

        # получение запроса с попыткой добавить пользователя копилке
        response = self.client.post(self.path, data)

        # проверка, что пользователь был действительно добавлен
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.path)

        self.bank.refresh_from_db()
        self.assertTrue(self.bank.users.filter(username='AnotherUser').exists())

    def test_edit_bank_post_add_user_error(self):
        data = self.data
        data['new_user'] = self.another_user

        # получение запроса с попыткой добавить пользователя
        response = self.client.post(self.path, data)

        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, self.path)

        # получение запроса с попыткой добавить повторно
        response = self.client.post(self.path, data)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertFormError(response, 'form', 'new_user', 'Пользователь уже был ранее добавлен!')