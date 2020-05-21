from kryptonite.models.models import Currency, FavouriteCurrency, FavouriteExchange, Exchange


def get_favourite_currencies(user_id):
    return [fav.currency for fav in FavouriteCurrency.objects.filter(user_id=user_id).select_related('currency')]


def get_favourite_exchanges(user_id):
    return [fav.exchange for fav in FavouriteExchange.objects.filter(user_id=user_id).select_related('exchange')]


def get_all_currencies():
    return Currency.objects.all()


def get_all_exchanges():
    return Exchange.objects.all()