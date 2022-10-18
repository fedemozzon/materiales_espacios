from cmath import inf, pi
from datetime import date, datetime, tzinfo
from zoneinfo import available_timezones
from django.shortcuts import render
import json
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Factory_Place, Material, Material_Provider, Material_arrived, Reserve_Factory
import jwt
from rest_framework_swagger.views import get_swagger_view

@csrf_exempt
def login(request):
    body = json.loads(request.body)
    print(body.get('username'))
    token = jwt.encode({"username": body.get('username'), "exp":1371720939}, algorithm='HS256', key='secret')
    print(token)
 
# Query para probar el método 
# localhost:8000/ask_for_material/?id_material=4&date_expected=2022-11-19&cant=100   
@api_view(['GET'])
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


@csrf_exempt
@api_view(['PUT'])
def stock_update(request):
    body = json.loads(request.body)
    material_id = body.get('material_id')
    provider_id = body.get('provider_id')
    amount = body.get('amount')
    material_provider = list(Material_Provider.objects.all().filter(material_id = int(material_id), provider_id = int(provider_id)).values_list())
    if(material_provider == []):
        return JsonResponse({"message": "No se encontro el material con el proveedor"})
    else:
        actual_amount = material_provider[0][3]
        Material_Provider.objects.filter(material_id = int(material_id), provider_id = int(provider_id)).update(total_amount= int(amount) + actual_amount)
        return JsonResponse({"La cantidad ha sido actualizada a ": actual_amount + int(amount)})
    
@csrf_exempt
@api_view(['POST'])
def reserve(request):
    request_body = json.loads(request.body)
    date_start = datetime.strptime(request_body.get('date_start'), '%Y-%m-%d')
    date_end = datetime.strptime(request_body.get('date_end'), '%Y-%m-%d')
    available_spaces = find_avalivable_place(date_start,date_end)
    factory_place_id = request_body.get('factory_place_id')
    print("lugares disponibles")
    print(type(available_spaces) == str)
    if(type(available_spaces) == str):
        return JsonResponse({"message": "No hay lugares disponibles en esa fecha"})
    else:
        if( int(factory_place_id) not in available_spaces):
            return JsonResponse({"message": "No hay lugares disponibles en esa fecha"})
        else:
            factory = Factory_Place.objects.get(id = request_body.get('factory_place_id'))
            Reserve_Factory.objects.create(factory_place_id = factory, date_start = date_start, date_end = date_end, enterprise = request_body.get('enterprise'), state = request_body.get('state'))
            return JsonResponse({"message": "El lugar ha sido reservado"})

 # /find_place/?date_start=2023-12-9&date_end=2023-12-30
@csrf_exempt
@api_view(['GET'])
def find_place_by_dates(request):
    date_start = datetime.strptime(request.GET.get('date_start'), '%Y-%m-%d')
    date_end = datetime.strptime(request.GET.get('date_end'), '%Y-%m-%d')
    return JsonResponse({"Message": find_avalivable_place(date_start, date_end)})

def find_avalivable_place(date_start, date_end):
    places = list(Factory_Place.objects.all().values_list())
    places = list(map(lambda place: place[0], places))
    reservation = list(Reserve_Factory.objects.all().values_list())
    for place in reservation:
        print(place[2])
        print(place[3])
        print(date_start)
        print(place[2].replace(tzinfo = None) <= date_start <= place[3].replace(tzinfo = None))
    unavaliable_places = list(filter(lambda place: (place[2].replace(tzinfo = None) <= date_start <= place[3].replace(tzinfo = None) ), reservation))
    unavaliable_places = list(map(lambda place: place[1], unavaliable_places))
    available_places = list(filter(lambda place: place not in unavaliable_places, places))
    print(available_places)
    if(available_places != []):
        return available_places
    else:
        return "No hay lugares disponibles en esa fecha"