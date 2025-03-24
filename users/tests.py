from unittest.mock import patch

from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.backends import PhoneBackend
from users.models import User


class RegisterViewTestCase(APITestCase):
    def test_register_new_user(self):
        url = reverse("users:register")
        data = {"phone": "+79991234567"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.filter(phone=data["phone"]).exists())

    def test_register_existing_user(self):
        user = User.objects.create(phone="+79991234567")
        url = reverse("users:register")
        data = {"phone": user.phone}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)

    def test_register_with_invite_code(self):
        inviter = User.objects.create(phone="+79991112233", invite_code="INV123")
        url = reverse("users:register")
        data = {"phone": "+79991234567", "invited_by": "INV123"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_user = User.objects.get(phone=data["phone"])
        self.assertEqual(new_user.invited_by, inviter)

    def test_register_with_existing_invite_code(self):
        inviter = User.objects.create(phone="+79991112233", invite_code="INV123")
        user = User.objects.create(phone="+79991234567", invited_by=inviter)
        url = reverse("users:register")
        data = {"phone": user.phone, "invited_by": "NEWCODE"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("invited_by", response.data)


class VerifyCodeViewTestCase(APITestCase):
    def test_verify_correct_code(self):
        user = User.objects.create(phone="+79991234567")
        code = user.generate_code()
        url = reverse("users:verify_code")
        data = {"phone": user.phone, "code": code}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_verify_wrong_code(self):
        user = User.objects.create(phone="+79991234567")
        url = reverse("users:verify_code")
        data = {"phone": user.phone, "code": "9999"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["message"], "Неверный код")


class UserProfileViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(phone="+79991234567")
        self.client.force_authenticate(user=self.user)

    def test_get_user_profile(self):
        url = reverse("users:user_profile")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["phone"], self.user.phone)


# class SendSMSViewTestCase(APITestCase):
#     @patch("users.services.send_sms", return_value={"success": True})
#     def test_send_sms_success(self, mock_send_sms):
#         url = reverse("users:send_sms")
#         data = {"phone": "+79991234567"}  # Плюс не должен быть в номере, преобразуйте его, если нужно.
#         response = self.client.post(url, data, follow=True)
#
#         # Проверяем статус
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#         # Проверяем, что send_sms был вызван с правильными аргументами
#         mock_send_sms.assert_called_once_with(79991234567, "Привет")
#
#     @patch("users.services.send_sms", return_value={"success": True})
#     def test_send_sms_no_phone(self, mock_send_sms):
#         url = reverse("users:send_sms")
#         response = self.client.post(url, {})  # Не передаем телефон в запросе
#
#         # Проверяем редирект
#         self.assertEqual(response.status_code, status.HTTP_302_FOUND)
#
#         # Проверяем, что send_sms не был вызван
#         mock_send_sms.assert_not_called()


class PhoneLoginViewTestCase(APITestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("authapp:phone_login")

    def test_phone_login_view(self):
        response = self.client.post(self.url, {"phone": "+79991234567"})
        self.assertEqual(response.status_code, 302)  # Должен быть редирект
        self.assertEqual(self.client.session["phone"], "+79991234567")


class PhoneConfirmViewTestCase(APITestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(phone="+79991234567")
        self.code = self.user.generate_code()
        session = self.client.session
        session["phone"] = self.user.phone
        session.save()
        self.url = reverse("authapp:phone_confirm")

    def test_phone_confirm_view_success(self):
        response = self.client.post(self.url, {"code": self.code})
        self.assertEqual(response.status_code, 302)  # Должен быть редирект

    def test_phone_confirm_view_wrong_code(self):
        response = self.client.post(self.url, {"code": "999999"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Неверный код")


class PhoneBackendTest(TestCase):

    def setUp(self):
        """Создаем пользователя для тестов"""
        self.user = User.objects.create(phone="+79991234567")
        # Генерация кода для пользователя
        self.code = self.user.generate_code()

    @patch("users.models.User.objects.get")
    def test_authenticate_success(self, mock_get_user):
        """Тест на успешную аутентификацию пользователя по телефону и коду"""
        mock_get_user.return_value = self.user

        backend = PhoneBackend()
        authenticated_user = backend.authenticate(
            None, phone="+79991234567", code=self.code
        )

        # Проверяем, что пользователь аутентифицирован
        self.assertEqual(authenticated_user, self.user)
        mock_get_user.assert_called_once_with(phone="+79991234567")

    @patch("users.models.User.objects.get")
    def test_authenticate_user_not_found(self, mock_get_user):
        """Тест, если пользователь с таким телефоном не найден"""
        mock_get_user.side_effect = User.DoesNotExist

        backend = PhoneBackend()
        authenticated_user = backend.authenticate(
            None, phone="+79991234567", code=self.code
        )

        # Проверяем, что возвращается None, если пользователь не найден
        self.assertIsNone(authenticated_user)

    @patch("users.models.User.objects.get")
    def test_get_user_success(self, mock_get_user):
        """Тест на получение пользователя по id"""
        mock_get_user.return_value = self.user

        backend = PhoneBackend()
        user = backend.get_user(self.user.id)

        self.assertEqual(user, self.user)
        mock_get_user.assert_called_once_with(pk=self.user.id)

    @patch("users.models.User.objects.get")
    def test_get_user_not_found(self, mock_get_user):
        """Тест, если пользователь не найден по id"""
        mock_get_user.side_effect = User.DoesNotExist

        backend = PhoneBackend()
        user = backend.get_user(self.user.id)

        self.assertIsNone(user)
