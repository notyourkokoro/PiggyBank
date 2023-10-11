from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, FormView, DeleteView
from django.views.generic import TemplateView

from common.mixins import TitleMixin
from banks.models import Bank
from banks.forms import CreateBankForm, EditBankProfileForm, AddMoneyForm


class IndexView(TitleMixin, TemplateView):
    template_name = 'banks/index.html'
    title = 'Главная'


class BanksView(TitleMixin, SuccessMessageMixin, FormView):
    template_name = 'banks/banks.html'
    form_class = AddMoneyForm
    success_message = 'Копилка успешно пополнена!'
    success_url = reverse_lazy('banks:banks')
    title = 'Копилки'


class DeleteBankView(SuccessMessageMixin, DeleteView):
    model = Bank
    success_url = reverse_lazy('banks:banks')
    success_message = 'Копилка успешно удалена!'


class ExitBankView(SuccessMessageMixin, UpdateView):
    model = Bank
    template_name = 'banks/banks.html'
    success_url = reverse_lazy('banks:banks')
    success_message = 'Вы успешно расстроили друга и покинули копилку!'
    fields = []

    def form_valid(self, form):
        bank = self.object
        user = self.request.user
        bank.users.remove(user)

        return super().form_valid(form)


class CreateBanksView(TitleMixin, SuccessMessageMixin, CreateView):
    model = Bank
    form_class = CreateBankForm
    template_name = 'banks/create_bank.html'
    success_url = reverse_lazy('banks:banks')
    success_message = 'Добавлена новая копилка!'

    title = 'Создать копилку'

    def form_valid(self, form):
        user = self.request.user

        form.instance.owner = user
        bank = form.save()

        user.banks.add(bank)
        return super().form_valid(form)


class EditBankView(TitleMixin, SuccessMessageMixin, UpdateView):
    model = Bank
    form_class = EditBankProfileForm
    template_name = 'banks/bank_profile.html'
    success_message = 'Копилка успешно отредактирована!'

    title = 'Редактировать копилку'

    def get_success_url(self):
        return reverse_lazy('banks:edit_bank', args=(self.object.id,))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['current_user'] = self.request.user.username
        return kwargs
