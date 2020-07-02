from django.shortcuts import render
from django.shortcuts import redirect
import requests
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import HttpResponse
import json
import ast


@csrf_exempt
# receive post and make post request example
def index(request):
    print(request.body)
    return HttpResponse("OK")


@csrf_exempt
def add_user(request):
    body = json.loads(request.body)
    username, email, password, first_name, last_name = body["username"], body["email"], body[
        "password"], body["first_name"], body["last_name"]

    user = User.objects.create_user(username, email, password)

    user.first_name = first_name
    user.last_name = last_name

    user.save()

    return HttpResponse("OK")

    # body = json.loads(request.body)

    # if "id" in body:
    #     print(body["id"])
    #     print("here")
    #     post_data = json.dumps({"name": "sadaf"})
    #     response = requests.post("http://127.0.0.1:8000", data=post_data)
    # return HttpResponse("OK")

    # return redirect('http://stackoverflow.com/')

    # Create your views here.
