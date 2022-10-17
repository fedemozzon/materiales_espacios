from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Material, Material_Provider
import jwt

@csrf_exempt
def login(request):
    body = json.loads(request.body)
    print(body.get('username'))
    token = jwt.encode({"username": body.get('username'), "exp":1371720939}, algorithm='HS256', key='secret')
    print(token)
    
@csrf_exempt
def ask_for_material(request):
    id_material = request.GET.get('id_material')
    cant = request.GET.get('cant')
    stock =  Material_Provider.objects.all().filter(material_id = int(id_material)).values_list()
    print(list(stock))
    return JsonResponse({"materials": ''})

@csrf_exempt
def materials(request):
    materials = Material.objects.values_list()
    print(list(materials))
    return JsonResponse({"materials": list(materials)})
