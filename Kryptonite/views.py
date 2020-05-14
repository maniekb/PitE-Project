from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.shortcuts import render, redirect
from .models.forms import RegistrationForm
from .models.models import Currency, FavouriteCurrency, FavouriteExchange, Exchange
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import Http404
from django.contrib import messages
import sweetify
from Kryptonite.DataService.BinanceClient import BinanceClient
from Kryptonite.Clients.Poloniex.client import PoloniexClient
from datetime import datetime
import json

import logging

logger = logging.getLogger(__name__)


def index(request):
    if request.user.is_authenticated:
        return render(request, 'user_index.html')
    else:
        return render(request, 'index.html')


def getBinanceData(request):
    client = BinanceClient()
    symbol = request.GET['symbol']
    interval = request.GET['interval']
    date_start = datetime.strptime(request.GET['date_start'], "%a, %d %b %Y %H:%M:%S %Z")
    data = client.GetHistoricalDataWithInterval(symbol, interval, date_start)
    list = [{"open_time": x[0], "open": x[1]} for x in data]
    return JsonResponse(list, safe=False)


def getPoloniexData(request):
    client = PoloniexClient()
    symbol = request.GET['symbol']
    interval = _map_intervals(request.GET['interval'])
    date_start = datetime.strptime(request.GET['date_start'], "%a, %d %b %Y %H:%M:%S %Z")
    date_start = _timestamp_gmt_to_utc(date_start.timestamp())
    date_end = datetime.now().timestamp()
    data = client.get_chart_data(symbol, int(date_start), int(date_end), interval)
    li = [{"open_time": record.date, "open": record.open} for record in data]
    return JsonResponse(li, safe=False)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                sweetify.success(request, title='Success', icon='success', text='Registration successful',
                                 timer=5000, button='Ok')
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'register.html', {'form': form})

    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                sweetify.success(request, title='Success', icon='success', text='Login successful',
                                 timer=5000, button='Ok')
                return redirect('/')
            else:
                return render(request, 'login.html', {'form': form})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def logout_user(request):
    logout(request)
    sweetify.success(request, title='Success', icon='success', text='You have been logged out',
                     timer=5000, button='Ok')
    return redirect('/')


@login_required
def favourites(request):
    c_ids = [fav.currency_id for fav in FavouriteCurrency.objects.filter(user_id=request.user.id)]

    all_currencies = Currency.objects.all()
    fav_curr = [curr for curr in all_currencies if curr.id in c_ids]
    rest_curr = [curr for curr in all_currencies if curr.id not in c_ids]

    e_ids = [fav.exchange_id for fav in FavouriteExchange.objects.filter(user_id=request.user.id)]

    all_exchanges = Exchange.objects.all()
    fav_exchange = [ex for ex in all_exchanges if ex.id in e_ids]
    rest_exchange = [ex for ex in all_exchanges if ex.id not in e_ids]
    return render(request, 'favourites.html',
                  {'currencies': rest_curr,
                   'curr_buttons': fav_curr,
                   "exchange_buttons": fav_exchange,
                   "exchanges": rest_exchange})


@login_required
def del_favourite_currency(request):
    if not request.is_ajax():
        raise Http404
    else:
        curr_id = request.POST.get("id", None)
        FavouriteCurrency.objects.filter(user_id=request.user.id, currency_id=curr_id).delete()
        return JsonResponse({"id": curr_id})


@login_required
def add_favourite_currency(request):
    if not request.is_ajax():
        raise Http404
    else:
        curr_id = request.POST.get("id", None)
        fav = FavouriteCurrency(user_id=request.user.id, currency_id=curr_id)
        fav.save()
        return JsonResponse({"id": curr_id})


@login_required
def del_favourite_exchange(request):
    if not request.is_ajax():
        raise Http404
    else:
        exch_id = request.POST.get("id", None)
        FavouriteExchange.objects.filter(user_id=request.user.id, exchange_id=exch_id).delete()
        return JsonResponse({"id": exch_id})


@login_required
def add_favourite_exchange(request):
    if not request.is_ajax():
        raise Http404
    else:
        exch_id = request.POST.get("id", None)
        fav = FavouriteExchange(user_id=request.user.id, exchange_id=exch_id)
        fav.save()
        return JsonResponse({"id": exch_id})


@login_required
def account(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            sweetify.success(request, title='Success', icon='success', text='You successfully changed your password',
                             timer=5000, button='Ok')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account.html', {
        'form': form
    })


@login_required
def arbitrage(request):
    # TODO
    return render(request, 'arbitrage.html')


def _timestamp_gmt_to_utc(timestamp):
    return timestamp + 7200


def _map_intervals(interval):
    if interval == '5m':
        return 300
    if interval == '1h':
        return 1800
    if interval in ['1d', '1y']:
        return 86400
