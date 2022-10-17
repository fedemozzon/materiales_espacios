from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Material
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
    materials = list(Material.objects.values_list())
    mat = list(filter(lambda material: material[0] == int(id_material), materials))
    return JsonResponse({"materials": mat})

@csrf_exempt
def materials(request):
    materials = Material.objects.values_list()
    print(list(materials))
    return JsonResponse({"materials": list(materials)})
