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
# import decimal

user_signed_in = None


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
        # del exp['id']
        del exp['user_id']
        exp['category_name'] = category_name
        exp['amount'] = float(exp['amount'])
        exp['date'] = str(exp['date'])
    print(to_send)
    print("converting to json...")
    to_send = list(to_send)
    # post_data = json.dumps(to_send)
    # print(post_data)
    return JsonResponse(to_send, safe=False)


@csrf_exempt
def expense_delete(request):
    body = json.loads(request.body)
    to_be_deleted = body["id"]
    print(expense.objects.all())
    exp = expense.objects.filter(id=to_be_deleted)
    exp.delete()
    print(expense.objects.all())
    return HttpResponse("Deleted")


@csrf_exempt
def expense_edit(request):
    body = json.loads(request.body)

    requesting_user = body["username"]
    this_user = User.objects.get(username=requesting_user)
    general_user = User.objects.get(username="General")
    cats = purchase_category.objects.filter(
        user=this_user) | purchase_category.objects.filter(user=general_user)

    cats = cats.values()

    valid_cats = [c["category"] for c in cats]

    new_cat = body["category"].lower()

    found = False

    oID = body["id"]
    e = expense.objects.get(id=oID)

    try:
        float(body["amount"])
    except ValueError:
        return HttpResponse("Please enter a number.")

    for vc in valid_cats:
        if vc.lower() == new_cat:
            found = True
            e.category = purchase_category.objects.get(category=vc)

    if not found:
        return HttpResponse("Category Doesn't Exist. Please make it first.")

    for key, value in body.items():
        if key != "id" and key != "category":
            print(key)
            setattr(e, key, value)

    e.save()
    print(expense.objects.all())

    return HttpResponse("Deleted")
