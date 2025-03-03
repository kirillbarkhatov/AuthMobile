from django.contrib import messages
from django.contrib.auth import login
from django.core.cache import cache
from django.shortcuts import redirect
from django.views.generic import FormView, View
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from smsaero import SmsAeroException

from users.forms import CodeForm, PhoneForm
from users.models import User
from users.serializers import RegisterSerializer, UserSerializer, VerifyCodeSerializer
from users.services import generate_invite_code, normalize_phone, send_sms
from drf_yasg.utils import swagger_auto_schema


class RegisterView(APIView):
    """
    Эндпоинт для регистрации и/или авторизации пользователя.

    Ожидает номер телефона и, опционально, инвайт-код.
    Проверяет, существует ли пользователь, создаёт его при необходимости.
    Генерирует код подтверждения и отправляет его пользователю.
    """

    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RegisterSerializer, responses={200: 'Код отправлен'})
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data["phone"]
            invited_by_code = serializer.validated_data.get("invited_by")

            # Проверяем, существует ли пользователь с таким номером
            user, created = User.objects.get_or_create(phone=phone)

            if not created:  # Если пользователь уже существует
                if (
                    user.invited_by and invited_by_code
                ):  # Если инвайт-код уже был установлен ранее
                    return Response(
                        {
                            "invited_by": "Инвайт-код уже указан и не может быть изменён."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # Устанавливаем инвайт-код, если он передан и ранее не был установлен
            if invited_by_code and not user.invited_by:
                invited_by_user = User.objects.filter(
                    invite_code=invited_by_code
                ).first()
                if invited_by_user:
                    user.invited_by = invited_by_user
                    user.save()

            # Генерация и отправка кода
            code = user.generate_code()
            # send_sms_code(phone, code)  # Отправляем код пользователю
            print(code)

            return Response({"message": "Код отправлен"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(APIView):
    """
    Эндпоинт для проверки кода подтверждения.

    Ожидает номер телефона и код подтверждения.
    Проверяет корректность кода и, в случае успеха, выдаёт JWT-токены.
    """

    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=VerifyCodeSerializer, responses={200: 'Авторизация успешна'})
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data["phone"]
            code = serializer.validated_data["code"]
            user = User.objects.filter(phone=phone).first()
            if user and user.check_code(code):
                # Генерация JWT токенов
                refresh = RefreshToken.for_user(user)
                return Response(
                    {"refresh": str(refresh), "access": str(refresh.access_token)},
                    status=status.HTTP_200_OK,
                )
                return Response(
                    {"message": "Авторизация успешна"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"message": "Неверный код"}, status=status.HTTP_403_FORBIDDEN
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveAPIView):
    """
    Эндпоинт для получения информации о пользователе.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class SendSMSView(View):
    """Контроллер для отправки СМС через сторонний сервис"""


    def post(self, request):
        # Получаем номер телефона из формы
        phone_number = request.POST.get("phone")

        # Пример обработки номера телефона
        if phone_number:
            print(f"Введённый номер телефона: {phone_number}")
            # Здесь можно добавить логику проверки номера телефона, аутентификации и т.д.
        else:
            messages.error(request, "Номер телефона обязателен для заполнения.")
            return redirect("authapp:login")  # Редирект обратно на страницу входа

        try:
            result = send_sms(int(phone_number), "Привет")
            print(result)
        except SmsAeroException as e:
            print(f"An error occurred: {e}")
        return redirect("authapp:login")


class PhoneLoginView(FormView):
    """Контроллер для авторизации в веб-интерфейсе - генерация кода"""

    template_name = "users/phone_login.html"  # Шаблон, который будет отображаться
    form_class = PhoneForm  # Форма для ввода телефона

    def post(self, request, *args, **kwargs):
        phone = request.POST.get("phone")
        phone = normalize_phone(phone)
        request.session["phone"] = phone
        user, created = User.objects.get_or_create(
            phone=phone
        )  # Получаем или создаем пользователя
        code = user.generate_code()  # Генерация кода
        # send_sms_code(phone, code)  # Отправляем код пользователю
        return redirect("authapp:phone_confirm")


class PhoneConfirmView(FormView):
    """Контроллер для авторизации в веб-интерфейсе - подтверждение кода"""

    template_name = "users/phone_confirm.html"
    form_class = CodeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        phone = self.request.session.get("phone")
        cached_code = cache.get(f"user_{phone}_code")
        context["cached_code"] = cached_code
        return context

    def post(self, request, *args, **kwargs):
        phone = request.session.get("phone")  # Получаем номер телефона из сессии
        code = request.POST.get("code")

        user = User.objects.filter(phone=phone).first()
        if user and user.check_code(code):
            login(
                request, user, backend="users.backends.PhoneBackend"
            )  # Логиним пользователя
            return redirect("authapp:index")
        else:
            form = self.get_form()
            form.add_error("code", "Неверный код")
            return self.form_invalid(form)
