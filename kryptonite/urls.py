from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/data/binance', views.get_historical_binance_data, name='api-data-binance'),
    path('api/data/poloniex', views.get_historical_poloniex_data, name='api-data-poloniex'),
    path('api/data/bitmex', views.get_historical_bitmex_data, name='api-data-bitmex'),
    path('register', views.register, name='register'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('arbitrage', views.arbitrage, name='arbitrage'),
    path('account', views.account, name='account'),
    path('favourites', views.favourites, name='favourites'),
    path('all', views.all_data_page, name='all_data'),
    path('del_favourite_currency', views.del_favourite_currency, name='del_favourite_currency'),
    path('add_favourite_currency', views.add_favourite_currency, name='add_favourite_currency'),
    path('add_favourite_exchange', views.add_favourite_exchange, name='add_favourite_exchange'),
    path('del_favourite_exchange', views.del_favourite_exchange, name='del_favourite_exchange')
]
