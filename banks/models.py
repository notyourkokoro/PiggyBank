from django.db import models
from django.db.models import CharField, DateTimeField, ManyToManyField, ForeignKey, CASCADE, DecimalField
from django.forms import ValidationError

from enum import Enum

from users.models import User


class Currency(Enum):
    dollar = 'USD'
    euro = 'EUR'
    ruble = 'RUB'


class Bank(models.Model):
    name = CharField(max_length=255)
    description = CharField(null=True, blank=True)

    goal = DecimalField(max_digits=10, decimal_places=2)
    current = DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = CharField(max_length=3, choices=[(c.value, c.name) for c in Currency], default=Currency.dollar.value)

    owner = ForeignKey(User, on_delete=CASCADE)
    created_timestamp = DateTimeField(auto_now_add=True)

    users = ManyToManyField(User, related_name='banks')

    def percent(self):
        return int(round(self.current / self.goal, 2) * 100)

    def add_user(self, new_user):
        if self.users.filter(username=new_user.username):
            raise ValidationError('Пользователь уже был ранее добавлен!')
        self.users.add(new_user)
