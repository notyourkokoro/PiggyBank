from django.contrib.auth.decorators import login_required
from django.urls import path

from banks.views import BanksView, CreateBanksView, EditBankView, DeleteBankView, ExitBankView

app_name = 'banks'

urlpatterns = [
    path('', login_required(BanksView.as_view()), name='banks'),
    path('create/', login_required(CreateBanksView.as_view()), name='create_bank'),
    path('edit/<int:pk>/', login_required(EditBankView.as_view()), name='edit_bank'),
    path('delete/<int:pk>/', login_required(DeleteBankView.as_view()), name='delete_bank'),
    path('exit/<int:pk>/', login_required(ExitBankView.as_view()), name='exit_bank'),
]
