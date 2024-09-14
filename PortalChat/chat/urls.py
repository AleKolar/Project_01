from django.urls import path

from . import views
from .views import registration_view, verify_code_view, home, LoginUser, login_user

urlpatterns = [
    path('signup/', registration_view, name='registration'),
    # path('', login_user, name='login'),
    # path('login', login_user, name='login'),
    path('profile/', login_user, name='login_user'),
    path('', LoginUser.as_view(), name='login'),
    path('login/', LoginUser.as_view(), name='login'),
    path('verify/', verify_code_view, name='verify_code'),
    path('home', home, name='home'),

    path('user/responses/', views.user_responses, name='user_responses'),
    path('response/delete/<int:response_id>/', views.delete_response, name='delete_response'),
    path('response/accept/<int:response_id>/', views.accept_response, name='accept_response'),

    path('private/', views.user_responses, name='private'),


]