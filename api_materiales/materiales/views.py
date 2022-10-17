from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import jwt

@csrf_exempt
def login(request):
    body = json.loads(request.body)
    print(body.get('username'))
    token = jwt.encode({"username": body.get('username'), "exp":1371720939}, algorithm='HS256', key='secret')
    print(token)
    
@csrf_exempt
def ask_for_material(request):
    print(request)
    return JsonResponse({"username": "capo"})
