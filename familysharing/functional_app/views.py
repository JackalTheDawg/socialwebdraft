import datetime

from django.shortcuts import render, redirect
from authorization_app.forms import *
from authorization_app import views as authapp_views
from django.http import HttpResponse
from FS_chat import views as chat_views
from .models import *
from .forms import *
import mimetypes

def first_page(request):
    """Авторизация"""
    user_creation_form = Create_user(request.POST)
    registration_form = Registarion_form(request.POST, request.FILES)
    form = Sign_in_form(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            user_data = form.cleaned_data
            checking_user = authapp_views.sign_in(user_data, request)
            return redirect(f'/id={checking_user}')
        """Регистрация"""
    if request.method == 'POST':
        if registration_form.is_valid() and user_creation_form.is_valid():
            account_data = user_creation_form.cleaned_data
            registration_data = registration_form.cleaned_data
            creation_user = authapp_views.sign_up(account_data, registration_data, request)
            return redirect(f'/id={creation_user}')
    context = {'sign_in_form': form, 'user_form': user_creation_form, 'registration_form': registration_form}
    return render(request, 'login_page.html', context)


def profile_info(user_id):
    """Функция возвращающая context содержащий данные профиля"""
    user_date = User_profile.objects.get(user=user_id)
    if user_date is not None:
        name = user_date.first_name
        second_name = user_date.second_name
        picture = user_date.profile_picture
        birthday = user_date.birthday
        birthday_month = user_date.birthday_month
        birthday_year = user_date.birthday_year
        context = {
            'name': name,
            'second_name': second_name,
            'picture': picture,
            'birthday': birthday,
            'birthday_month': birthday_month,
            'birthday_year': birthday_year
            }
        return context
    else:
        return HttpResponse('Something goes wrong')


def users_page(request, page_id):
    """ Отрисовка страницы"""
    if request.user.id is not None:
        posts_authors = {}
        visitor = User.objects.get(pk=request.user.id)
        user = User.objects.get(pk=page_id)
        context = profile_info(page_id)
        posts = reversed(Users_blog.objects.filter(page=user.id))
        for post in posts:
            post_author = User_profile.objects.get(user=post.author)
            result = {post: post_author}
            posts_authors.update(result)

        form = Blog_form(request.POST, request.FILES)
        context.update({'id': request.user.id,
                        'page_id': user,
                        'posts': posts_authors,
                        'form': form})
        if request.method == 'POST':
            if form.is_valid():
                post = form.cleaned_data
                Users_blog.objects.create(author=visitor,
                                          blog=post['blog'],
                                          content=post['content'],
                                          date=datetime.datetime.now(),
                                          page=page_id)
                return redirect(f'/id={page_id}')
        return render(request, 'page.html', context)
    else:
        return HttpResponse('Sign in for view this page')

def redirect_on_personal_page(request):
    """Редирект на личную страницу"""
    if User.is_authenticated:
        user_id = request.user.id
        return redirect(f'/id={user_id}')

def search_page(request):
    """Выводит на странице поиска информацию по всем пользователям, запускает функцию поиска"""
    users = User_profile.objects.all()
    context = {'users': users}
    search_query = request.GET.get('q', None)
    if search_query is not None:
        query_set = search(search_query)
        results = {'results': query_set}
        return render(request, 'search.html', results)
    return render(request, 'search.html', context)

def search(search_atribbut):
    """Принимает на вход запрос, обрабатывает наличие в базе и возвращает результат поиска в виде query set"""
    username = User_profile.objects.filter(first_name__icontains=search_atribbut)
    user_second_name = User_profile.objects.filter(second_name__icontains=search_atribbut)
    if username.exists() is not False:
        return username
    elif user_second_name.exists() is not False:
        return user_second_name
    else:
        return None

