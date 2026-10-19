from .utils import generate_pin, lookup_hash, make_key
from cryptography.fernet import Fernet
from django.shortcuts import render, redirect
from .models import Drop, Stats
import secrets

def get_stats(request):
    stats, _ = Stats.objects.get_or_create(id=1)
    return stats

def home(request):
    stats = get_stats()
    return render(request, "base.html", {"stats": stats})

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

            stats = get_stats()
            stats.created = stats.created + 1
            stats.save()

            request.session["new_pin"] = pin
            return redirect("pin_page")

    return render(request, "create_drop_box.html")

def retrive_drop(request):
    text_url, error, lookup = None, None, None

    if request.method == "POST":
        pin = request.POST.get("pin", "").strip().upper()
        magic_word = request.POST.get("magic_word", "").strip()

        lookup = lookup_hash(pin, magic_word)
        drop = Drop.objects.filter(lookup=lookup).first()

        if drop:
            stats = get_stats()
            stats.retrived = stats.retrived + 1
            stats.save()

            text_url = Fernet(make_key(pin, magic_word, drop.salt)).decrypt(drop.drop.encode()).decode()
            request.session.pop("new_pin", None)
        else:
            error = "Wrong PIN or magic word"
            lookup = None

    return render(request, "open_drop.html", {"text_url": text_url, "error": error, "lookup": lookup})

def destroy_drop(request):
    if request.method == "POST":
        lookup = request.POST.get("lookup", "")
        Drop.objects.filter(lookup=lookup).delete()

        stats = get_stats()
        stats.destroyed = stats.destroyed + 1
        stats.save()

        request.session.pop("new_pin", None)

    return redirect("home")

def pin_page(request):
    pin = request.session.get("new_pin")

    if not pin:
        return redirect("cbd")

    return render(request, "pin_page.html", {"pin": pin})

def clear_pin(request):
    request.session.pop("new_pin")
    return redirect("home")