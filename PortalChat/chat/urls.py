from django.urls import path
from .views import registration_view, verify_code_view, home, LoginUser, login_user

urlpatterns = [
    path('signup/', registration_view, name='registration'),
    # path('', login_user, name='login'),
    # path('login', login_user, name='login'),
    path('profile/', login_user, name='login_user'),
    path('', LoginUser.as_view(), name='login'),
    path('login/', LoginUser.as_view(), name='login'),
    path('verify/', verify_code_view, name='verify_code'),
    path('home', home, name='registration_success'),


]