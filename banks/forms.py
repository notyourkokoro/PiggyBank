from django.forms import (
    ModelForm, CharField, TextInput, 
    Textarea, DecimalField, NumberInput, 
    ChoiceField, Select, ValidationError,
    IntegerField, HiddenInput
)

from banks.models import Bank, Currency
from users.models import User


class CreateBankForm(ModelForm):
    name = CharField(
        widget=TextInput(
            attrs={
                'class': 'form-control form-control-lg'
            }
        ),
    )

    description = CharField(
        widget=Textarea(
            attrs={
                'class': 'form-control form-control-lg'
            }
        ),
        required=False
    )

    goal = DecimalField(
        widget=NumberInput(
            attrs={
                'class': 'form-control form-control-lg'
            },
        ),
    )

    currency = ChoiceField(
        widget=Select(
            attrs={
                'class': 'form-control form-control-lg'
            },
        ),
        choices=[(c.value, c.value) for c in Currency]
    )

    class Meta:
        model = Bank
        fields = ('name', 'description', 'goal', 'currency')


class EditBankProfileForm(CreateBankForm):
    new_user = CharField(
        widget=TextInput(
            attrs={
                'class': 'form-control form-control-lg'
            }
        ),
        required=False
    )

    class Meta:
        model = Bank
        fields = ('name', 'description', 'goal', 'currency', 'new_user')

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)

    def clean_new_user(self):
        new_user_username = self.cleaned_data['new_user']
        if new_user_username:
            if new_user_username == self.current_user:
                raise ValidationError('Вы не можете добавить самого себя!')

            new_user = User.objects.filter(username=new_user_username).first()

            if not new_user:
                raise ValidationError('Никого нет с таким именем пользователя!')

            self.instance.add_user(new_user)
        return new_user_username

    def clean_goal(self):
        goal = self.cleaned_data['goal']
        if self.instance.current > goal:
            raise ValidationError('Текущие накопления не могут превышать новую цель!')
        return goal


class AddMoneyForm(ModelForm):
    money = DecimalField(
        widget=NumberInput(
            attrs={
                'class': 'form-control form-control-lg'
            },
        ),
    )

    class Meta:
        model = Bank
        fields = ('money',)

    def clean_money(self):
        bank = Bank.objects.get(pk=self.data['bank_id'])
        money = self.cleaned_data['money']

        print(bank.current, bank.goal)
        if money > bank.goal - bank.current:
            raise ValidationError('В копилке не может содержаться денег больше, чем цель!')
        bank.current = bank.current + money
        bank.save()
        return money
