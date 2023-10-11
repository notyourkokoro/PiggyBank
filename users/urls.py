from django.urls import path

from django.contrib.auth.decorators import login_required
from users.views import UserRegistrationView, UserLoginView, UserProfileView, DeleteUserView
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', login_required(LogoutView.as_view()), name='logout'),
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    path('delete/<int:pk>/', login_required(DeleteUserView.as_view()), name='delete_user'),
]
