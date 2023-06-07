from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from authorization_app.forms import *
from django.contrib.auth.models import User
from functional_app import models

def sign_in(authorization_data, request):
    """Функция авторизации"""
    try:
        user = authenticate(username=authorization_data['login'],
                            password=authorization_data['password'])

        if user is not None:
            if user.is_active:
                login(request, user)
                return user.id
        else:
            return HttpResponse('Disabled account')
    except User.DoesNotExist:
        return HttpResponse('Disabled account')

def sign_up(account_data, registration_data ,request):
    """Регистрация"""
    try:
        User.objects.get(email=account_data['email']) ### Добавить логин через амперсанд
        return HttpResponse('login or email is already using')
    except User.DoesNotExist:
        User.objects.create_user(username=account_data['username'],
                                 password=account_data['password'],
                                 email=account_data['email'])
        user = authenticate(username=account_data['username'],
                            password=account_data['password'])
        login(request, user)
        user = User.objects.get(pk=user.id)
        models.User_profile.objects.create(first_name=registration_data['first_name'],
                                           second_name=registration_data['second_name'],
                                           sex=registration_data['sex'],
                                           birthday=registration_data['birthday'],
                                           birthday_month=registration_data['birthday_month'],
                                           birthday_year=registration_data['birthday_year'],
                                           profile_picture=registration_data['profile_picture'],
                                           user=user)
        return user.id

def check_session(request):
    """Проверки сессии"""
    if request.user.id is not None:
        return redirect(f'/id={request.user.id}')
    else:
        return redirect('home/')