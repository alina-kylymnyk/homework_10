from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from bson.objectid import ObjectId
# from .forms import QuoteForm

# Create your views here.
from .utils import get_mongodb


def main(request, page=1):
   db = get_mongodb()
   quotes = db.quotes.find()
   per_page = 10
   paginator = Paginator(list(quotes), per_page)
   quotes_on_page = paginator.page(page)
   return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})



def author_quotes(request, author_id):
    db = get_mongodb()
    # Перетворюємо рядок ID в ObjectId
    try:
        author_id = ObjectId(author_id)
    except Exception as e:
        # Якщо перетворення не вдалося, відобразити помилку
        return render(request, '404.html', status=404)

    # Отримуємо інформацію про автора
    author = db.authors.find_one({"_id": author_id})
    if not author:
        return render(request, '404.html', status=404)

    # Отримуємо всі цитати для конкретного автора
    quotes = list(db.quotes.find({"author": author_id}))

    return render(request, 'quotes/author_quotes.html', {'author': author, 'quotes': quotes})


# def quote(request):
#     if request.method == 'POST':
#         form = QuoteForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('quotes:root')  # Після успішного збереження перенаправлення на головну сторінку
#     else:
#         form = QuoteForm()

#     # Використовується правильний шлях до шаблону
#     return render(request, 'quotes/quote.html', {'form': form})

