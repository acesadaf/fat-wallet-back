from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponse
from backend.models import *
from backend.utils.check_tokens import *
import json
import ast
from django.http import JsonResponse
# import decimal

user_signed_in = None


@csrf_exempt
def expense_data(request):
    body = json.loads(request.body)
    if not valid_token(body):
        return HttpResponse("Invalid Token")
    requesting_user = body["username"]
    this_user = User.objects.get(username=requesting_user)
    expenses = expense.objects.filter(user=this_user)
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

    to_send = list(to_send)
    return JsonResponse(to_send, safe=False)


@csrf_exempt
def expense_delete(request):
    body = json.loads(request.body)
    if not valid_token(body):
        return HttpResponse("Invalid Token")
    to_be_deleted = body["id"]
    exp = expense.objects.filter(id=to_be_deleted)
    exp.delete()
    return HttpResponse("Deleted")


@csrf_exempt
def expense_edit(request):
    body = json.loads(request.body)
    if not valid_token(body):
        return HttpResponse("Invalid Token")
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
            setattr(e, key, value)

    e.save()

    return HttpResponse("Deleted")
