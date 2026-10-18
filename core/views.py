from .utils import generate_pin, lookup_hash, make_key
from cryptography.fernet import Fernet
from django.shortcuts import render
from .models import Drop
import secrets

def home(request):
    return render(request, "base.html")

def create_drop_box(request):
    return render(request, "create_drop_box.html")

def retrive_drop_box(request):
    return render(request, "retrive_drop_box.html")

def create_drop(request):
    if request.method == "POST":
        drop = request.POST.get("drop", "").strip()
        magic_word = request.POST.get("magic_word", "").strip()

        if drop and magic_word:
            pin = generate_pin()

            while Drop.objects.filter(lookup=lookup_hash(pin, magic_word)).exists():
                pin = generate_pin()

            salt = secrets.token_hex(16)
            token = Fernet(make_key(pin, magic_word, salt)).encrypt(drop.encode())

            Drop.objects.create(lookup=lookup_hash(pin, magic_word), salt=salt, drop=token.decode())
            return render(request, "pin_page.html", {"pin":pin})

    return render(request, "create_drop_box.html")

def retrive_drop(request):
    drop, error = None, None

    if request.method == "POST":
        pin = request.POST.get("pin", "").strip().upper()
        magic_word = request.POST.get("magic_word", "").strip()

        drop = Drop.objects.filter(lookup=lookup_hash(pin, magic_word)).first()

        if drop:
            text_url = Fernet(make_key(pin, magic_word, drop.salt)).decrypt(drop.drop.encode()).decode()
        else:
            error = "Wrong PIN or magic word"

    return render(request, "open_drop.html", {"text_url": text_url, "error": error})
