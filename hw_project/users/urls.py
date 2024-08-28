from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [ 
    path('signup/', views.signup_user, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('quotes/', views.quote_list, name='quote_list'),

    

]
