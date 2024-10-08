from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from . import views
from .views import registration_view, home, LoginUser, login_user, AdvertisementCreateView, \
    AdvertisementUpdateView, verify_code_view, NewsletterCreateView, display_news, CustomLogoutView
from django.urls import path

# router = DefaultRouter()
# router.register(r'your-endpoint', NewsletterCreateView, basename='your-unique-basename')
# router.register(r'your-endpoint', NewsletterCreateAPIView, basename='your-unique-basename')

urlpatterns = [
    path('signup/', registration_view, name='registration'),
    # path('', login_user, name='login'),
    # path('login', login_user, name='login'),
    path('profile/', login_user, name='login_user'),
    path('', LoginUser.as_view(), name='login'),
    path('login/', LoginUser.as_view(), name='login'),
    path('verify/', verify_code_view, name='verify_code'),

    path('home/', home, name='home'),
    # path('accounts/home/', home, name='home'),

    path('user/responses/', views.user_responses, name='user_responses'),
    path('response/delete/<int:response_id>/', views.delete_response, name='delete_response'),
    path('response/accept/<int:response_id>/', views.accept_response, name='accept_response'),

    path('private/', views.user_responses, name='private'),

    path('advertisement_create/', AdvertisementCreateView.as_view(), name='advertisement_create'),
    path('create_response/<int:advertisement_id>/', views.create_response, name='response_create'),

    path('accounts/create_response/<int:advertisement_id>/', views.create_response, name='response_create'),
    path('create_response/<int:advertisement_id>/', views.create_response, name='create_response'),

    path('response/accept/<int:response_id>/', views.accept_response, name='accept_response'),
    path('accounts/create_response/<int:response_id>/', views.accept_response, name='accept_response'),
    path('accounts/accounts/create_response/<int:response_id>/', views.accept_response, name='accept_response'),


    path('advertisement/update/<int:pk>/', AdvertisementUpdateView.as_view(), name='advertisement_update'),

    # path('create/', NewsletterCreateAPIView.as_view(), name='create_newsletter_api'),
    path('createform/', NewsletterCreateView.as_view(), name='create_newsletter_form'),

    path('news/', display_news, name='news_page'),

    path('logout/', CustomLogoutView.as_view(), name='logout')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

