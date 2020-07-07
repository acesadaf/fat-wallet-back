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
def category_data(request):
    body = json.loads(request.body)
    requesting_user = body["username"]
    this_user = User.objects.get(username=requesting_user)
    general_user = User.objects.get(username="General")
    cat = purchase_category.objects.filter(
        user=this_user) | purchase_category.objects.filter(user=general_user)
    to_send = cat.values()
    for c in to_send:
        del c['user_id']
        del c['id']

    to_send = list(to_send)
    return JsonResponse(to_send, safe=False)

@csrf_exempt
def expense_submit(request):
    print("adding...")
    body = json.loads(request.body)
    name, amount, date_of_expense, category, description, user = body["name"], body[
        "amount"], body["date_of_expense"], body["category"], body["description"], body["user"]

    exp = expense(name=name, amount=amount, date=date_of_expense, category=purchase_category.objects.get(
        category=category), description=description, user=User.objects.get(username=user))
    exp.save()
    print(expense.objects.all())
    return HttpResponse("Expense Added")



@csrf_exempt
def category_submit(request):
    print("adding...")
    body = json.loads(request.body)
    name, category = body["name"], body["category"]
    try: 
        cat = purchase_category(user = User.objects.get(username = name), category=category)
        cat.save()
        # print(purchase_category.objects.all())
        return HttpResponse("Category Added")
    except:
        return HttpResponse("Failed to Add")

@csrf_exempt
def category_delete(request):
    print("deleting...")
    body = json.loads(request.body)
    name, cat = body["name"], body["category"]

    print(purchase_category.objects.all())
    purchase_category.objects.get(user = User.objects.get(username = name), category= cat).delete()
    print(purchase_category.objects.all())
    
    return HttpResponse("Category deleted")