import os

from django.db.models import Sum, Count, F, Q
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.forms import ModelForm
from .models import Transaction, CustomUser

from .helpers import lookup

# Create your views here.

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

class quoteForm(forms.Form):
    stock = forms.CharField(label='Stock')

class buyForm(forms.Form):
    symbol = forms.CharField(label="Stock Symbol",
                            widget=forms.TextInput(attrs={'placeholder': 'Stock Symbol'}))
    shares = forms.CharField(label="Number of Shares",
                            widget=forms.TextInput(attrs={'placeholder': 'Number of Shares'}))


def index(request):

    # Get the amount of cash a user has
    balance = CustomUser.objects.first().cash
     
    # Get the sum of all the SELLS; make it a negative number
    sale_total = Transaction.objects.filter(buysell='SELL').aggregate(Sum('price'))
    x, y = next(iter(sale_total.items()))
    sales = (0 - round(y, 2))
    
    # Get the sum of all the BUYS
    previous_buys = Transaction.objects.last()
    buy_total = Transaction.objects.filter(buysell="BUY").aggregate(Sum('price'))
    key, buys = next(iter(buy_total.items()))
    buys = round(buys, 2)

    # Get the last transaction (most recent)
    # If the number of shares is negative, make it positive
    last_transaction = Transaction.objects.last()
    if last_transaction.shares < 0:
        last_transaction.shares = (last_transaction.shares) + (-last_transaction.shares)
        # last_transaction.shares = last_transaction.shares ** 2
    
    add_up = float(sales) + float(buys)
    
    sub_total = float(add_up) * int(last_transaction.shares)

    grandtotal = float(balance) + float(sub_total)

    transactions = Transaction.objects.all()
    unique = {name.stock for name in transactions}

    for i in unique:
        share_total = Transaction.objects.values('stock', 'name', 'shares', 'price').annotate(Sum('shares'))
        # key, shares = next(iter(share_total.items()))


    return render(request, 'stocks/index.html', {
        # 'transaction': transactions,
        'share_total': share_total,
        'nathan_cash': balance,
        'grandtotal': grandtotal,
    })

def buy(request):
    if request.method == "GET":
        return render(request, "stocks/buy.html", {
            "form": buyForm()
        })
    else:
        form = buyForm(request.POST)

        if form.is_valid():
            symbol = form.cleaned_data["symbol"]
            shares = form.cleaned_data["shares"]
            stock_info = lookup(symbol)
            total_amount = stock_info["price"] * int(shares)

            user_cash = CustomUser.objects.first().cash

            if user_cash < total_amount:
                return render(request, "stocks/apology.html", {
                'message': "Sorry, insufficent funds to make this purchase."
            })
        
            balance = float(user_cash) - float(total_amount)
            buy = "BUY"
            shares_bought = int(shares)
            nathan = CustomUser.objects.first()

            n = Transaction(user=nathan, stock=symbol, name=stock_info['name'], price=stock_info['price'], shares=shares,
                            buysell=buy)
            n.save()

            nathan.cash = balance
            nathan.save()

            return HttpResponseRedirect('/stocks/')



def sell(request):

    if request.method == "GET":
        rows = Transaction.objects.all()
        symbols = []

        for row in rows:
            symbols.append(row.stock)

        symbols = list(set(symbols))
        data = []
        # for symbol in symbols:
        #     data.append(symbol)
        for symbol in symbols:
            share_total = Transaction.objects.filter(stock=symbol).aggregate(Sum('shares'))
            key, shares = next(iter(share_total.items()))
            
            if shares > 0:
                data.append(symbol)
        
        return render(request, "stocks/sell.html", {
            "data": data
        })
    else:
       
        if request.method == 'POST':

            symbol = request.POST.get("symbol")
            shares = int(request.POST.get("shares"))

            quote = lookup(symbol)
            current_price = quote["price"]

            sell_price = float(current_price) * int(shares)
            sold_shares = 0 - int(shares)
            sell = 'SELL'

            nathan = CustomUser.objects.first()
            user_cash = nathan.cash

            n = Transaction(user=nathan, stock=symbol, price=current_price, shares=sold_shares,
                                buysell=sell)
            n.save()

            balance = float(user_cash) + float(sell_price)
            nathan.cash = balance
            nathan.save()
           
            return HttpResponseRedirect('/stocks/')

def history(request):
    return render(request, 'stocks/history.html', {
        'transaction': Transaction.objects.all(),
    })

def quote(request):
    if request.method == "GET":
        return render(request, "stocks/quote.html", {
            "form": quoteForm()
        })
    else:
        form = quoteForm(request.POST)

        if form.is_valid():
            symbol = form.cleaned_data["stock"]
            quote = lookup(symbol)
            return render(request, "stocks/quoted.html", {
            'message': quote
        })

