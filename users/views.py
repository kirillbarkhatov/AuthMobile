from django.contrib.auth.models import AbstractUser
from django.core.cache import cache
from django.db import models
from django.http import JsonResponse

from users.services import generate_invite_code, send_sms, normalize_phone

from django.views.generic import View, FormView
from django.contrib import messages


from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from users.models import User
from users.serializers import UserSerializer, RegisterSerializer, VerifyCodeSerializer

from smsaero import SmsAeroException

from django.shortcuts import render, redirect
from django.contrib.auth import login
from users.forms import PhoneForm, CodeForm

from django.urls import reverse_lazy
from django.db import IntegrityError






class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            user, created = User.objects.get_or_create(phone=phone)
            return Response({"message": "Код отправлен"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Авторизация успешна"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SendSMSView(View):
    def post(self, request):
        # Получаем номер телефона из формы
        phone_number = request.POST.get('phone')

        # Пример обработки номера телефона
        if phone_number:
            print(f"Введённый номер телефона: {phone_number}")
            # Здесь можно добавить логику проверки номера телефона, аутентификации и т.д.
        else:
            messages.error(request, "Номер телефона обязателен для заполнения.")
            return redirect('users:login')  # Редирект обратно на страницу входа


        try:
            result = send_sms(int(phone_number), "Привет")
            print(result)
        except SmsAeroException as e:
            print(f"An error occurred: {e}")
        return redirect('users:login')


class PhoneLoginView(FormView):
    template_name = 'users/phone_login.html'  # Шаблон, который будет отображаться
    form_class = PhoneForm  # Форма для ввода телефона

    def post(self, request, *args, **kwargs):
        phone = request.POST.get('phone')
        phone = normalize_phone(phone)
        request.session['phone'] = phone
        user, created = User.objects.get_or_create(phone=phone)  # Получаем или создаем пользователя
        code = user.generate_code()  # Генерация кода
        # send_sms_code(phone, code)  # Отправляем код пользователю
        return redirect('authapp:phone_confirm')


class PhoneConfirmView(FormView):
    template_name = 'users/phone_confirm.html'
    form_class = CodeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        phone = self.request.session.get('phone')
        cached_code = cache.get(f"user_{phone}_code")
        context["cached_code"] = cached_code
        return context

    def post(self, request, *args, **kwargs):
        phone = request.session.get('phone')  # Получаем номер телефона из сессии
        code = request.POST.get('code')

        user = User.objects.filter(phone=phone).first()
        if user and user.check_code(code):
            login(request, user, backend='users.backends.PhoneBackend')  # Логиним пользователя
            return redirect('authapp:index')
        else:
            form = self.get_form()
            form.add_error('code', 'Неверный код')
            return self.form_invalid(form)
