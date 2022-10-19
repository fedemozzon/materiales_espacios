from cmath import inf, pi
from datetime import datetime, tzinfo
from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Factory_Place, Material, Material_Provider, Material_arrived, Reserve_Factory
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework_swagger.views import get_swagger_view

# Query para probar el método 
# localhost:8000/ask_for_material/?id_material=4&date_expected=2022-11-19&cant=100   
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def ask_for_material(request):
    id_material = request.GET.get('id_material')
    date_expected = request.GET.get('date_expected')
    cant = request.GET.get('cant')
    return JsonResponse({"materials": get_providers_for_material(id_material, date_expected, cant)})

@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
def materials(request):
    materials = Material.objects.values_list()
    return JsonResponse({"materials": list(materials)})

@permission_classes([permissions.IsAuthenticated])
def compromised_materials_for_provider(id_provider,expected_date, id_material):
    expected_date = datetime.strptime(expected_date, '%Y-%m-%d')
    materials = Material_arrived.objects.all().filter(provider_id = int(id_provider), material_id = int(id_material)).values_list()
    materials_in_date = filter(lambda material: datetime.now()<= material[4].replace(tzinfo = None) <= expected_date, materials)
    return sum(map(lambda material: material[3], materials_in_date))

@permission_classes([permissions.IsAuthenticated])
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
@permission_classes([permissions.IsAuthenticated])
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
@permission_classes([permissions.IsAuthenticated])
def reserve(request):
    request_body = json.loads(request.body)
    
    Reserve_Factory.objects.create(factory_place_id = request_body.get('factory_place_id'), date_start = request_body.get('date_start'), date_end = request_body.get('date_end'), enterprise = request_body.get('enterprise'), state = request_body.get('state'))
    return JsonResponse({"message": "Reserva creada exitosamente"})

@csrf_exempt
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def find_place_by_dates(request):
    date_start = datetime.strptime(request.GET.get('date_start'), '%Y-%m-%d')
    date_end = datetime.strptime(request.GET.get('date_end'), '%Y-%m-%d')
    factory_id = int(request.GET.get('factory_place_id'))
    caca = list(Reserve_Factory.objects.all().values_list())
    places = list(Reserve_Factory.objects.all().filter(factory_place_id = factory_id).values_list())
    if(places == []):
        return JsonResponse({"message": "No existe un lugar con ese ID"})
    else:
        places_in_date = list(filter(lambda place: date_start >= place[3].replace(tzinfo = None), places))
        if(places_in_date != []):
            print(places_in_date)
            return JsonResponse({"places": places_in_date})
        else:
            return JsonResponse({"message": "No hay lugares disponibles en esa fecha"})