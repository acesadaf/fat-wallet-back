from django.shortcuts import render
from django.shortcuts import redirect
import requests
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponse
from backend.models import *
import json
import ast
from django.http import JsonResponse
import datetime
from django.db.models import Sum
#import decimal

user_signed_in = None


@csrf_exempt
def category_wise_user_data(request):
    body = json.loads(request.body)
    requesting_user = body["username"]
    this_user = User.objects.get(username=requesting_user)
    expenses = expense.objects.filter(user=this_user).values()
    category_wise = {}
    for e in expenses:
        e['amount'] = float(e['amount'])
        cat_id = e['category_id']
        category_name = purchase_category.objects.get(id=cat_id).category
        category_wise[category_name] = category_wise.get(
            category_name, 0) + e['amount']

    return JsonResponse(category_wise)

    #general_user = User.objects.get(username="General")


@csrf_exempt
def monthly_user_data(request):
    body = json.loads(request.body)
    requesting_user, count, month_or_week = body["username"], body["duration"], body["month_or_week"]
    this_user = User.objects.get(username=requesting_user)
    # month_wise = {}

    today = datetime.date.today()
    print(today)
    month = ["January", "February", "March", "April", "May", "June",
             "July", "August", "September", "October", "November", "December"]

    monthly_expense = {}
    for e in range(count-1, -1, -1):
        if today.month-e-1 < 0:
            temp = list(expense.objects.filter(user=this_user, date__year=today.year-1,
                                               date__month=12 + (today.month-e)).aggregate(Sum('amount')).values())[0]
            if temp != None:
                monthly_expense[month[today.month - e - 1]] = float(temp)
            else:
                monthly_expense[month[today.month - e - 1]] = float(0)
        else:
            temp = list(expense.objects.filter(user=this_user, date__year=today.year,
                                               date__month=today.month-e).aggregate(Sum('amount')).values())[0]
            if temp != None:
                monthly_expense[month[today.month - e - 1]] = float(temp)
            else:
                monthly_expense[month[today.month - e - 1]] = float(0)

    return JsonResponse(monthly_expense)
