import logging
import random
import string

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView

from .filters import filter_user_responses
from .forms import RegistrationForm, ConfirmationForm, AdvertisementForm, ResponseForm
from django import forms
from .tasks import send_confirmation_code, send_one_time_code_email, send_response_notification_task, \
    send_response_email
from .models import CustomUser, Advertisement, Response, Newsletter
from .forms import AuthForm


def generate_confirmation_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def clean_email(self):
    email = self.cleaned_data['email']
    if CustomUser.objects.filter(email=email).exists():
        raise forms.ValidationError("Такой E-mail уже существует!")
    return email


def confirm_code(request):
    if request.method == 'POST':
        form = ConfirmationForm(request.POST)
        if form.is_valid():
            code_entered = form.cleaned_data['code']
            user = request.user
            code_stored = user.customuser.code

            if code_entered == code_stored:

                return redirect('home')
            else:
                return redirect('registration')

    else:
        form = ConfirmationForm()

    return render(request, 'confirm_code_template.html', {'form': form})


# РЕГИСТРАЦИЯ
def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            code = generate_confirmation_code()
            user.code = code
            user.save()
            expiration_time = timezone.now() + timedelta(seconds=120)
            send_one_time_code_email.delay(user.pk)

            print(f'One-time code generated: {code}')

            return render(request, 'verify_code.html', {'form': form})
        else:
            return render(request, 'registration.html', {'form': form})
    else:
        form = RegistrationForm()
        return render(request, 'registration.html', {'form': form})


# ВВОДИМ КОД ПОДТВЕРЖДЕНИЯ
def verify_code_view(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        user = CustomUser.objects.get(code=code)
        user.is_verified = True
        user.save()
        return render(request, 'home.html')
    return render(request, 'verify_code.html')


# ОТПРАВЛЯЕТ КОД НА ПОЧТУ
def login_user(request):
    if request.user.is_authenticated:
        user = request.user

        send_confirmation_code.delay(user.pk)
        print(f'Confirmation code sent to user: {user.code}')

        return redirect('verify_code')

    return render(request, 'login.html', {'form': AuthenticationForm()})



# def login_user(request):
#     if request.method == 'POST':
#         form = AuthForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             username = form.cleaned_data['username']
#             code = generate_confirmation_code()
#             request.session['confirmation_code'] = code
#
#             user = authenticate(request, username=username, password=password)
#
#             if user is not None:
#                 send_confirmation_code.delay(user.pk)
#
#                 print(f'Confirmation code sent to user: {code}')
#
#                 return redirect('verify_code')
#
#     else:
#         form = AuthForm()
#
#     return render(request, 'login.html', {'form': form})


# ВХОД (АВТОРИЗАЦИЯ)
class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    extra_context = {'title': "Авторизация"}

    def form_valid(self, form):
        response = super().form_valid(form)

        user = self.request.user
        code = generate_confirmation_code()
        user.code = code
        user.save()
        send_confirmation_code.delay(user.id)

        return response


# ЗАРЕГИСТРИРОВАННЫХ НАДЕЛЯЕМ ПОЛНОМОЧИЯМИ



# ДОМАШНЯЯ
def home(request):
    all_responses = Response.objects.all()
    all_advertisements = Advertisement.objects.all().order_by('-advertisement_id')
    admin_news = Newsletter.objects.filter(sent_date__isnull=False)

    paginator = Paginator(all_advertisements, 10)  # Разбиваем объявления на страницы, по 10 объявлений на страницу
    page = request.GET.get('page')

    try:
        all_advertisements = paginator.page(page)
    except PageNotAnInteger:
        all_advertisements = paginator.page(1)
    except EmptyPage:
        all_advertisements = paginator.page(paginator.num_pages)

    return render(request, 'home.html',
                  {'all_responses': all_responses, 'all_advertisements': all_advertisements, 'admin_news': admin_news})




# СОЗДАЕМ ОБЪЯВЛЕНИЕ С МЕДИА
logger = logging.getLogger(__name__)


# class AdvertisementCreateView(LoginRequiredMixin, CreateView):
#     model = Advertisement
#     fields = ['title', 'text', 'category', 'image']
#     template_name = 'advertisement_create.html'
#
#     # success_url = reverse_lazy('home')
#     def get_success_url(self):
#         from django.urls import reverse
#         return reverse('home')
#
#     @login_required
#     def form_valid(self, form):
#         form.instance.user_id = self.request.user.id
#         category = form.cleaned_data.get('category')
#         valid_categories = ['Tanks', 'Healers', 'DPS', 'Traders', 'Guild Masters', 'Quest Givers', 'Blacksmiths',
#                             'Leatherworkers', 'Alchemists', 'Spellcasters']
#
#         if category not in valid_categories:
#             form.add_error('category',
#                            'Выберите категорию из списка: Танки, Хилы, ДД, Торговцы, Гилдмастеры, Квестгиверы, Кузнецы, Кожевники, Зельевары, Мастера заклинаний')
#             logger.error('Выбранная категория не допустима: %s', category)
#             return self.form_invalid(form)
#
#         return super().form_valid(form)
#
#     def post(self, request, *args, **kwargs):
#         form = self.get_form()
#         if form.is_valid():
#             logger.info('Данные формы действительны. Попытка сохранения в базу данных.')
#             return self.form_valid(form)
#         else:
#             logger.error('Данные формы недействительны.')
#             return self.form_invalid(form)



class AdvertisementCreateView(CreateView):
    model = Advertisement
    fields = ['title', 'text', 'category', 'image']
    template_name = 'advertisement_create.html'

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        category = form.cleaned_data.get('category')
        valid_categories = ['Tanks', 'Healers', 'DPS', 'Traders', 'Guild Masters', 'Quest Givers', 'Blacksmiths',
                            'Leatherworkers', 'Alchemists', 'Spellcasters']

        if category not in valid_categories:
            form.add_error('category',
                           'Выберите категорию из списка: Танки, Хилы, ДД, Торговцы, Гилдмастеры, Квестгиверы, Кузнецы, Кожевники, Зельевары, Мастера заклинаний')
            return self.form_invalid(form)

        return super().form_valid(form)

    success_url = reverse_lazy('home')





# ДЛЯ ФИЛЬТРАЦИИ ОТКЛИКОВ ПОЛЬЗ-ЛЯ
def user_responses(request, advertisement_id=None):
    form = AdvertisementForm()
    user_id = request.user.id
    user_responses = filter_user_responses(user_id, title=request.GET.get('title'),
                                           category=request.GET.get('category'), advertisement_id=advertisement_id)

    return render(request, 'private.html', {'form': form, 'user_responses': user_responses})

# СОЗДАЮ ОТКЛИК
@login_required
def create_response(request, advertisement_id):
    advertisement = Advertisement.objects.get(advertisement_id=advertisement_id)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['content']
            user = request.user
            response = Response(user=user, advertisement=advertisement, content=text)
            response.save()
            send_response_notification_task.delay(advertisement_id, text)
            return redirect('home')
    else:
        form = ResponseForm()

    return render(request, 'create_response.html', {'form': form, 'advertisement_id': advertisement_id})

# ОТПРАВКА УВЕДОМЛЕНИЙ

def send_response_notification(advertisement, response_text):
    send_response_email(advertisement, response_text)


# ДЛЯ ПРИВАТНОЙ СИРАНИЦЫ, ГДЕ ОТКЛИКИ СОЗДАННЫЕ ПОЛЬЗОВАТЕЛЕМ
# def user_responses(request):
#     form = AdvertisementForm()
#     user_responses = Response.objects.filter(user=request.user)
#
#     # Фильтрация по id объявления
#     # advertisement_id = request.GET.get('advertisement_id')
#     # if advertisement_id:
#     #     user_responses = user_responses.filter(advertisement_id=advertisement_id)
#
#     # Фильтрация по названию объявления
#     advertisement_title = request.GET.get('title')
#     if advertisement_title:
#         user_responses = user_responses.filter(advertisement__title=advertisement_title)
#
#     # Фильтрация по категории объявления
#     category = request.GET.get('category')
#     if category:
#         user_responses = user_responses.filter(advertisement__category=category)
#
#     return render(request, 'private.html', {'form': form, 'user_responses': user_responses})




def delete_response(request, response_id):
    response = get_object_or_404(Response, id=response_id)
    response.delete()
    return redirect('private')


def accept_response(request, response_id):
    response = get_object_or_404(Response, id=response_id)

    # Здесь доп. логика, что-то , ещё, нужно/можно
    response.published = True
    response.save()

    # Отправка уведомления user, оставившему отклик
    send_response_notification_task.delay(response.advertisement.id, response.text)

    return redirect('private')
