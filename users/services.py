import random
import string


def generate_invite_code():
    """Генерирует 6-значный инвайт-код."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))