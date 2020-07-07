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