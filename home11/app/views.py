from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return HttpResponse("""
        <h1>Главная</h1>
        <ul>
            <li><a href='/about/'>О сайте</a></li>
            <li><a href='/contacts/'>Контакты</a></li>
             <li><a href='/users/'>Пользователи</a></li>
        </ul>
    """)

def about(request):
    return HttpResponse("""
        <h1>О сайте</h1>
        <p>Мини-приложение на Django:)</p>
        <button> 
        <a href='/'>На главную</a>
        </button>
    """)

def contacts(request):
    return render(request, "contacts.html")

def users(request):
    return render(request, "users.html")