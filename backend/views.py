from django.shortcuts import render
from django.shortcuts import redirect
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
import ast


@csrf_exempt
# receive post and make post request example
def index(request):
    print(request.body)
    body = json.loads(request.body)

    if "id" in body:
        print(body["id"])
        print("here")
        post_data = json.dumps({"name": "sadaf"})
        response = requests.post("http://127.0.0.1:8000", data=post_data)
    return HttpResponse("OK")

    # return redirect('http://stackoverflow.com/')

    # Create your views here.
