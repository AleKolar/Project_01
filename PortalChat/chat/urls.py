from django.urls import path
from .views import registration_view, login_user, verify_code_view, home

urlpatterns = [
    path('signup/', registration_view, name='registration'),
    path('', login_user, name='login'),
    path('login', login_user, name='login'),
    path('verify/', verify_code_view, name='verify_code'),
    path('home', home, name='registration_success'),


]