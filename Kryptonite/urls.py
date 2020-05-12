from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/data/', views.get_data, name='api-data'),
    path('register', views.register, name='register'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('arbitrage', views.arbitrage, name='arbitrage'),
    path('account', views.account, name='account'),
    path('favourites', views.favourites, name='favourites'),
    path('del_favourite_currency', views.del_favourite_currency, name='del_favourite_currency'),
    path('add_favourite_currency', views.add_favourite_currency, name='add_favourite_currency'),
    path('add_favourite_exchange', views.add_favourite_exchange, name='add_favourite_exchange'),
    path('del_favourite_exchange', views.del_favourite_exchange, name='del_favourite_exchange')
]
