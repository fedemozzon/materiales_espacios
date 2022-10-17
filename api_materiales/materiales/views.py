from datetime import datetime, tzinfo
from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Material, Material_Provider, Material_arrived
import jwt

@csrf_exempt
def login(request):
    body = json.loads(request.body)
    print(body.get('username'))
    token = jwt.encode({"username": body.get('username'), "exp":1371720939}, algorithm='HS256', key='secret')
    print(token)
 
# Query para probar el método 
# localhost:8000/ask_for_material/?id_material=4&date_expected=2022-11-19&cant=100   
@csrf_exempt
def ask_for_material(request):
    id_material = request.GET.get('id_material')
    date_expected = request.GET.get('date_expected')
    cant = request.GET.get('cant')
    return JsonResponse({"materials": get_providers_for_material(id_material, date_expected, cant)})

@csrf_exempt
def materials(request):
    materials = Material.objects.values_list()
    return JsonResponse({"materials": list(materials)})

def compromised_materials_for_provider(id_provider,expected_date, id_material):
    expected_date = datetime.strptime(expected_date, '%Y-%m-%d')
    materials = Material_arrived.objects.all().filter(provider_id = int(id_provider), material_id = int(id_material)).values_list()
    materials_in_date = filter(lambda material: datetime.now()<= material[4].replace(tzinfo = None) <= expected_date, materials)
    return sum(map(lambda material: material[3], materials_in_date))

def get_providers_for_material(id_material, date_expected, cant):
    providers_list = []
    providers_for_material =  Material_Provider.objects.all().filter(material_id = int(id_material)).values_list()
    for provider in list(providers_for_material):
        if( provider[3] > int(cant)):
            providers_list.append({"id_provider": provider[2]})
        else:
            if((compromised_materials_for_provider(provider[2], date_expected, id_material) + provider[3]) > int(cant)):
                providers_list.append({"id_provider": provider[2]})
    return providers_list