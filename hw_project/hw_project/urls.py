from django.contrib import admin
from django.urls import path, include
from quotes import views  # Import views from the 'quotes' app


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quotes.urls')),
    # path ('quote/', views.quote, name='quote'),
    path('users/', include('users.urls')),
    path('author/<str:author_id>/', views.author_quotes, name='author_quotes'),
    
    
    ]
