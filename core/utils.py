import base64, hashlib, secrets, string
from django.conf import settings

def generate_pin():
    letter = string.ascii_uppercase
    digit = string.digits

    pin = secrets.choice(letter) + secrets.choice(digit) + secrets.choice(letter) + secrets.choice(digit)
    return pin

def lookup_hash(pin, magic_word):
    return hashlib.sha256((settings.SECRET_KEY + pin + magic_word).encode()).hexdigest()

def make_key(pin, magic_word, salt):
    raw = hashlib.pbkdf2_hmac("sha256", (pin + magic_word).encode(), bytes.fromhex(salt), 200_000)
    return base64.urlsafe_b64encode(raw)