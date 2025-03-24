import random
import string

from phonenumbers import PhoneNumberFormat, format_number, parse
from smsaero import SmsAero

from config.settings import SMSAERO_API_KEY

SMSAERO_EMAIL = "79110920294@mail.ru"


def send_sms(phone: int, message: str) -> dict:
    """
    Sends an SMS message

    Parameters:
    phone (int): The phone number to which the SMS message will be sent.
    message (str): The content of the SMS message to be sent.

    Returns:
    dict: A dictionary containing the response from the SmsAero API.
    """
    api = SmsAero(SMSAERO_EMAIL, SMSAERO_API_KEY)
    return api.send_sms(phone, message)


def normalize_phone(phone):
    parsed_phone = parse(phone, "RU")  # Парсим номер телефона
    return format_number(
        parsed_phone, PhoneNumberFormat.E164
    )  # Приводим к международному формату


def generate_invite_code():
    """Генерирует 6-значный инвайт-код."""
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
