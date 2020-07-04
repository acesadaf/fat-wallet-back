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
# receive post and make post request example
def index(request):
    print(request.body)
    return HttpResponse("OK")


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
def add_user(request):
    print("registering...")
    body = json.loads(request.body)
    username, email, password, first_name, last_name = body["username"], body["email"], body[
        "password"], body["first_name"], body["last_name"]

    user = User.objects.create_user(username, email, password)

    user.first_name = first_name
    user.last_name = last_name

    user.save()

    return HttpResponse("Added")


@csrf_exempt
def sign_in(request):
    global user_signed_in
    body = json.loads(request.body)
    username, password = body["username"], body["password"]
    user = authenticate(username=username, password=password)

    if user is not None:

        user_signed_in = username
        print("Signed in:", user_signed_in)
        return HttpResponse("Signed in!")
    else:
        return HttpResponse("No users with those credentials.")

    # body = json.loads(request.body)

    # if "id" in body:
    #     print(body["id"])
    #     print("here")
    #     post_data = json.dumps({"name": "sadaf"})
    #     response = requests.post("http://127.0.0.1:8000", data=post_data)
    # return HttpResponse("OK")

    # return redirect('http://stackoverflow.com/')

    # Create your views here.


@csrf_exempt
def category_submit(request):
    print("adding...")
    body = json.loads(request.body)
    category = body["category"]

    cat = purchase_category(category=category)
    cat.save()
    print(purchase_category.objects.all())
    return HttpResponse("Category Added")


@csrf_exempt
def expense_data(request):
    body = json.loads(request.body)
    requesting_user = body["username"]
    this_user = User.objects.get(username=requesting_user)
    expenses = expense.objects.filter(user=this_user)
    print(expenses)
    print("removing id and user_id...")
    to_send = expenses.values()
    for exp in to_send:
        cat_id = exp['category_id']
        category_name = purchase_category.objects.get(id=cat_id).category
        del exp['category_id']
        del exp['id']
        del exp['user_id']
        exp['category_name'] = category_name
        exp['amount'] = float(exp['amount'])
        exp['date'] = str(exp['date'])
    print(to_send)
    print("converting to json...")
    to_send = list(to_send)
    #post_data = json.dumps(to_send)
    # print(post_data)
    return JsonResponse(to_send, safe=False)
