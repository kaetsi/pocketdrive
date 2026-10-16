from django.shortcuts import render

def home(request):
    return render(request, "base.html")

def create_drop_box(request):
    return render(request, "create_drop_box.html")

def retrive_drop_box(request):
    return render(request, "retrive_drop_box.html")