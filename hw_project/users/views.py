from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, LoginForm, AuthorForm, QuoteForm
from .models import Quote
from pymongo import MongoClient
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy


def get_mongodb():
    client = MongoClient('mongodb://localhost')
    db = client.hw
    return db

def signup_user(request):
    if request.user.is_authenticated:
        return redirect('users:login')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='users:profile')
        else:
            return render(request, 'users/signup.html', context={"form": form})

    return render(request, 'users/signup.html', context={"form": RegisterForm()})


def login_user(request):
    if request.user.is_authenticated:
        return redirect('users:profile')

    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            messages.error(request, 'Username or password didn\'t match')
            return redirect(to='users:login')

        login(request, user)
        return redirect('users:profile')

    return render(request, 'users/login.html', context={"form": LoginForm()})


@login_required
def logout_user(request):
    logout(request)
    return redirect('quotes:root')


from django.shortcuts import render, redirect
from .forms import AuthorForm, QuoteForm
from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient('mongodb://localhost')
db = client.hw

@login_required
def profile(request):
    db = get_mongodb()

    if not request.user.is_authenticated:
        return redirect('login')  # Перенаправлення на сторінку входу, якщо не залогінений

    # Отримуємо всі цитати, які додав користувач
    user_quotes = list(db.quotes.find({"user": request.user.username}))
    for quote in user_quotes:
        author_id = quote['author']['$oid']
        quote['author'] = db.authors.find_one({"_id": ObjectId(author_id)})

    return render(request, 'profile.html', {'quotes': user_quotes})

@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            author_data = {
                "fullname": form.cleaned_data['fullname'],
                "born_date": form.cleaned_data['born_date'],
                "born_location": form.cleaned_data['born_location'],
                "description": form.cleaned_data['description']
            }
            db.authors.insert_one(author_data)
            return redirect('users:profile')  # Перенаправлення на список цитат
    else:
        form = AuthorForm()

    return render(request, 'users/add_author.html', {'form': form})

@login_required
def add_quote(request):
    authors = list(db.authors.find())  # Отримуємо всіх авторів для форми
    if request.method == 'POST':
        form = QuoteForm(request.POST, authors=authors)
        if form.is_valid():
            quote_data = {
                "quote": form.cleaned_data['quote'],
                "tags": [tag.strip() for tag in form.cleaned_data['tags'].split(',')] if form.cleaned_data['tags'] else [],
                "author": ObjectId(form.cleaned_data['author']),  # Зберігаємо ID автора
                "user": request.user.username  # Вказуємо ім'я користувача
            }
            db.quotes.insert_one(quote_data)
            return redirect('users:profile')
    else:
        form = QuoteForm(authors=authors)

    return render(request, 'users/add_quote.html', {'form': form})

@login_required
def quote_list(request):
    db = get_mongodb()
    quotes = list(db.quotes.find())  # Отримуємо всі цитати
    for quote in quotes:
        quote['author'] = db.authors.find_one({"_id": ObjectId(quote['author'])})  # Знаходимо автора для кожної цитати
    return render(request, 'quote_list.html', {'quotes': quotes})


@login_required
def profile_view(request):
    return render(request, 'users/profile.html')  # або інший шаблон для профілю

@login_required
def user_quotes_view(request):
    # Фільтрація цитат за поточним користувачем
    quotes = Quote.objects.filter(user=request.user)
    return render(request, 'users/profile.html', {'quotes': quotes})



class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'users/password_reset_subject.txt'
