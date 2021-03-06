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
def category_data(request):
    body = json.loads(request.body)
    if not valid_token(body):
        return HttpResponse("Invalid Token")
    requesting_user = body["username"]
    this_user = User.objects.get(username=requesting_user)
    general_user = User.objects.get(username="General")
    cat = purchase_category.objects.filter(
        user=this_user) | purchase_category.objects.filter(user=general_user)
    to_send = cat.values()
    for c in to_send:
        user_id = c['user_id']
        username = User.objects.get(id=user_id).username
        del c['user_id']
        del c['id']
        c['username'] = username

    to_send = list(to_send)
    return JsonResponse(to_send, safe=False)


@csrf_exempt
def expense_submit(request):
    body = json.loads(request.body)
    if not valid_token(body):
        return HttpResponse("Invalid Token")
    name, amount, date_of_expense, category, description, user = body["name"], body[
        "amount"], body["date_of_expense"], body["category"], body["description"], body["user"]

    exp = expense(name=name, amount=amount, date=date_of_expense, category=purchase_category.objects.get(
        category=category), description=description, user=User.objects.get(username=user))
    exp.save()
    return HttpResponse("Expense Added")


@csrf_exempt
def category_submit(request):
    body = json.loads(request.body)
    if not valid_token(body):
        return HttpResponse("Invalid Token")
    name, category = body["name"], body["category"]
    try:
        cat = purchase_category(user=User.objects.get(
            username=name), category=category)
        cat.save()
        return HttpResponse("Category Added")
    except:
        return HttpResponse("Failed to Add")


@csrf_exempt
def category_delete(request):
    body = json.loads(request.body)
    if not valid_token(body):
        return HttpResponse("Invalid Token")
    name, cat = body["name"], body["category"]

    purchase_category.objects.get(user=User.objects.get(
        username=name), category=cat).delete()

    return HttpResponse("Category deleted")


@csrf_exempt
def category_edit(request):
    body = json.loads(request.body)
    if not valid_token(body):
        return HttpResponse("Invalid Token")
    name, old_cat, new_cat = body["name"], body["old"], body["new"]

    edited_cat = purchase_category.objects.get(user=User.objects.get(
        username=name), category=old_cat)

    edited_cat.category = new_cat
    edited_cat.save()

    return HttpResponse("Category Edited")
