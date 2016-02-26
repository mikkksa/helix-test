# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from app import settings


def index(request):
    if 'cart' in request.session:
        cart = request.session.get('cart')
    else:
        request.session['cart'] = 0
        request.session['goods'] = []
        request.session['colors'] = []
        request.session['colorskot'] = []
    return render(request, 'engine/first.html', {'cart': request.session['cart']})

def robots(request):
    return render(request, 'engine/robots.txt')

def kotokota(request):
    if 'cart' in request.session:
        cart = request.session.get('cart')
    else:
        request.session['cart'] = 0
        request.session['goods'] = []
        request.session['colorskot'] = []
        request.session['colors'] = []
    if request.POST:
        colorhtml = [x for x in request.POST if x.startswith('color')]
        if 'addkot' in request.POST:
            request.session['cart'] += 1
            goods = request.session['goods']
            goods.append('kot')
            request.session['goods'] = goods
            try:
                color = colorhtml[0][5:]
                colors = request.session['colorskot']
                colors.append(color)
                request.session['colorskot'] = colors
            except:
                pass
            return redirect('/cart')
    return render(request, 'engine/kotokota.html', {'cart': request.session['cart']})

def sitemap1(request):
    return render(request, 'engine/sitemap.xml')

def kametta(request):
    if 'cart' in request.session:
        cart = request.session.get('cart')
    else:
        request.session['cart'] = 0
        request.session['goods'] = []
        request.session['colors'] = []
        request.session['colorskot'] = []
    if request.POST:
        colorhtml = [x for x in request.POST if x.startswith('color')]
        if 'addkam' in request.POST:
            request.session['cart'] += 1
            goods = request.session['goods']
            goods.append('kam')
            request.session['goods'] = goods
            try:
                color = colorhtml[0][5:]
                colors = request.session['colors']
                colors.append(color)
                request.session['colors'] = colors
            except:
                pass
            return redirect('/cart')
    return render(request, 'engine/kametta.html', {'cart': request.session['cart']})


def delivery(request):
    goods = []
    colors = []
    carT = 0
    if 'cart' in request.session:
        goods = request.session['goods']
        carT = request.session['cart']
        colors = request.session['colors']
    return render(request, 'engine/delivery.html', {'goods': goods, 'cart': carT})


def contacts(request):
    goods = []
    carT = 0
    if 'cart' in request.session:
        goods = request.session['goods']
        carT = request.session['cart']
    return render(request, 'engine/contacts.html', {'goods': goods, 'cart': carT})


def about(request):
    goods = []
    carT = 0
    if 'cart' in request.session:
        goods = request.session['goods']
        carT = request.session['cart']
    return render(request, 'engine/about.html', {'goods': goods, 'cart': carT})


def thank(request):
    goods = []
    carT = 0
    if 'cart' in request.session:
        goods = request.session['goods']
        carT = request.session['cart']
    return render(request, 'engine/thank.html', {'goods': goods, 'cart': carT})

def acs(request):
    goods = []
    carT = 0
    if 'cart' in request.session:
        goods = request.session['goods']
        carT = request.session['cart']
    return render(request, 'engine/acs.html', {'goods': goods, 'cart': carT})


def stol(request):
    goods = []
    carT = 0
    if 'cart' in request.session:
        goods = request.session['goods']
        carT = request.session['cart']
    return render(request, 'engine/stol.html', {'goods': goods, 'cart': carT})

def ogran(request):
    goods = []
    carT = 0
    if 'cart' in request.session:
        goods = request.session['goods']
        carT = request.session['cart']
    return render(request, 'engine/ogran.html', {'goods': goods, 'cart': carT})


def cart(request):
    goods = []
    goods1 = []
    colors = []
    colorskot = []
    carT = 0
    kams = 0
    kots = 0
    if 'cart' in request.session:
        goods = request.session['goods']
        carT = request.session['cart']
        try:
            colors = request.session['colors']
        except:
            pass
        try:
            colorskot = request.session['colorskot']
        except:
            pass
        for g in goods:
            if g == 'kam':
                kams += 1
            elif g == 'kot':
                kots += 1
    summ = kots * 4600 + 4860 * kams
    if request.POST:
        if 'deletec' in request.POST and 'cart' in request.session:
            del request.session['cart']
            del request.session['goods']
            del request.session['colors']
            del request.session['colorskot']
            return redirect('/cart')
        if 'format' in request.POST:
            return render(request, 'engine/format.html',
                          {'goods': goods, 'cart': carT, 'kots': kots, 'kams': kams, 'sum': summ,
                           'colors': request.session['colors'], 'colorskot': request.session['colorskot']})
        if 'save' in request.POST:
            try:
                kams = int(request.POST.get('num1'))
                kams_ = kams
                while kams_ >= 1:
                    goods1.append('kam')
                    kams_ -= 1
            except:
                pass
            try:
                kots = int(request.POST.get('num2'))
                kots_ = kots
                while kots_ >= 1:
                    goods1.append('kot')
                    kots_ -= 1
            except:
                pass
            request.session['goods'] = goods1
            request.session['cart'] = kams + kots
            return redirect('/cart')
        if 'send' in request.POST:
            fio = request.POST.get('fio')
            address = request.POST.get('address')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            result = fio + '\n' + address + '\n' + email + '\n' + phone + '\n'
            if kots == 0:
                send_mail('StulClick: новый заказ', result + str(kams) + ' каметта(цвета: ' + ','.join(
                colors) + ')', 'stulclick@stulclick.ru',
                      ['stulclick@stulclick.ru', email, 'mikel1998@mail.ru'], fail_silently=False)
            elif kams == 0:
                send_mail('StulClick: новый заказ', result + str(
                kots) + ' котокота(цвета: ' + ','.join(colorskot) + ')', 'stulclick@stulclick.ru',
                      ['stulclick@stulclick.ru', email, 'mikel1998@mail.ru'], fail_silently=False)
            else:
                send_mail('StulClick: новый заказ', result + str(
                    kots) + ' котокота(цвета: ' + ','.join(colorskot) + ') и ' + str(kams) + ' каметта(цвета: ' + ','.join(
                    colors) + ')', 'stulclick@stulclick.ru',
                        ['stulclick@stulclick.ru', email, 'mikel1998@mail.ru'], fail_silently=False)
            return redirect('/thank')
        if 'cont' in request.POST:
            try:
                if goods[len(goods)-1] == 'kot':
                    return redirect('/kotokota')
                else:
                    return redirect('/kametta')
            except:
                return redirect('/')
    return render(request, 'engine/cart.html', {'goods': goods, 'cart': carT, 'kots': kots, 'kams': kams, 'sum': summ,
                                                'colors': colors, 'colorskot': colorskot})	