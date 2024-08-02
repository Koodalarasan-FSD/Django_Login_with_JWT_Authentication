from django.urls import path
from .views import login_view, register_view, UserLoginView, UserRegisterView, protected_view

urlpatterns = [
    path('login', login_view, name='login_page'),
    path('register', register_view, name='register_page'),
    path('api/user/register/', UserRegisterView.as_view(), name='register'),
    path('api/user/login/', UserLoginView.as_view(), name='login'),
    path('protected_page/', protected_view, name='protected_page'),
]
