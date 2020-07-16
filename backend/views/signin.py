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
def add_user(request):
    print("registering...")
    body = json.loads(request.body)
    username, email, password, first_name, last_name = body["username"], body["email"], body[
        "password"], body["first_name"], body["last_name"]

    exists = ""
    try:
        User.objects.get(username=username)
        exists = "Username"
    except User.DoesNotExist:
        pass

    lst = User.objects.filter(email=email).values()
    if len(lst) != 0:
        if not exists:
            exists = "Email"
        else:
            exists += " and Email"

    if not exists:
        user = User.objects.create_user(username, email, password)

        user.first_name = first_name
        user.last_name = last_name

        user.save()
        return HttpResponse("Added")
    else:
        return HttpResponse(exists + " taken")


@csrf_exempt
def sign_in(request):
    global user_signed_in
    body = json.loads(request.body)
    username, password = body["username"], body["password"]
    user = authenticate(username=username, password=password)

    if user is not None:

        user_signed_in = username
        return HttpResponse("Signed in!")
    else:
        return HttpResponse("No users with those credentials.")


@csrf_exempt
def give_name(request):
    body = json.loads(request.body)
    username = body["username"]
    name = User.objects.get(username=username).first_name

    return HttpResponse(name)

    # body = json.loads(request.body)

    # if "id" in body:
    #     print(body["id"])
    #     print("here")
    #     post_data = json.dumps({"name": "sadaf"})
    #     response = requests.post("http://127.0.0.1:8000", data=post_data)
    # return HttpResponse("OK")

    # return redirect('http://stackoverflow.com/')

    # Create your views here.
