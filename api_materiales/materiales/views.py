from cmath import inf, pi
from datetime import date, datetime, tzinfo
from tracemalloc import start
from zoneinfo import available_timezones
from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework_swagger.views import get_swagger_view

# Query para probar el método 
# localhost:8000/ask_for_material/?id_material=4&date_expected=2022-11-19&cantidad=100   
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def ask_for_material(request):
    id_material = request.GET.get('id_material')
    date_expected = request.GET.get('date_expected')
    cantidad = request.GET.get('cantidad')
    return JsonResponse({"Providers": get_providers_for_material(id_material, date_expected, cantidad)})

@csrf_exempt
def materials(request):
    materials = Material.objects.values_list()
    return JsonResponse({"materials": list(materials)})

def compromised_materials_for_provider(id_provider,expected_date, id_material):
    expected_date = datetime.strptime(expected_date, '%Y-%m-%d')
    materials = Material_arrived.objects.all().filter(provider_id = int(id_provider), material_id = int(id_material)).values_list()
    materials_in_date = filter(lambda material: datetime.now()<= material[4].replace(tzinfo = None) <= expected_date, materials)
    return sum(map(lambda material: material[3], materials_in_date))

def get_providers_for_material(id_material, date_expected, cantidad):
    providers_list = []
    try:
        providers_for_material =  Material_Provider.objects.all().filter(material_id = int(id_material)).values_list()
        for provider in list(providers_for_material):
            if( provider[3] > int(cantidad)):
                provider_name= Provider.objects.get(id=int(provider[2])).name
                providers_list.append({"name_provider": provider_name, "id_provider": provider[2]})
            else:
                if((compromised_materials_for_provider(provider[2], date_expected, id_material) + provider[3]) > int(cantidad)):
                    provider_name= Provider.objects.get(id=int(provider[2])).name
                    providers_list.append({"name_provider": provider_name, "id_provider": provider[2]})
    except: 
        providers_list = 'Error en la consulta'
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

# Query para probar el método 
# localhost:8000/reserve_material/
""" {   
    "id_material":4,
    "id_provider":1,
    "id_sede":1,
    "id_empresa":1,
    "amount":100,
    "reserve_date":"2022-11-19"
}    """
@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def reserve_material(request):
    id_material = request.POST.get("id_material")
    id_provider = request.POST.get("id_provider")
    amount = request.POST.get("amount")
    reserve_date = request.POST.get("reserve_date")
    id_sede = request.POST.get("id_sede")
    id_empresa = request.POST.get("id_empresa")
    return JsonResponse(reserve_material_of_provider(id_material, id_provider, amount, reserve_date, id_sede, id_empresa))

def reserve_material_of_provider(id_material, id_provider, amount, reserve_date, id_sede, id_empresa):
    try:
        material_provider = Material_Provider.objects.all().filter(material_id=id_material, provider_id=id_provider)[0]
        material_provider.compromise_amount = material_provider.compromise_amount + int(amount)
        material_provider.save()
        newReserve = Reserve_material()
        material = Material.objects.get(id=id_material)
        provider = Provider.objects.get(id=id_provider)
        sede = Factory_Place.objects.get(id=id_sede)
        empresa = Enterprise.objects.get(id=id_empresa)
        newReserve.add(material, provider, amount, reserve_date, sede, empresa)
        newReserve.save()
        json = newReserve.strJson()
    except IndexError:
        return {"message":"No existe el material indicado para dicho proveedor"}
    except: 
        return {"message":"Error en la consulta"}
    return json

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def cancel_reserve_material(request):
    id_reserve = request.GET.get('id_reserve')
    try:
        reserve = Reserve_material.objects.get(id=id_reserve)
        material_provider = Material_Provider.objects.all().filter(material_id=reserve.material_id, provider_id=reserve.provider_id)[0]
        material_provider.compromise_amount = material_provider.compromise_amount - reserve.amount
        material_provider.save()
        delete = reserve.delete()
    except IndexError:
        return {"message": "No existe el material de dicho proveedor indicado en la reserva"}
    return JsonResponse({"message": "Eliminado correctamente"})
    
@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def reserve(request):
    request_body = json.loads(request.body)
    date_start = datetime.strptime(request_body.get('date_start'), '%Y-%m-%d')
    date_end = datetime.strptime(request_body.get('date_end'), '%Y-%m-%d')
    available_spaces = find_avalivable_place(date_start,date_end)
    factory_place_id = request_body.get('factory_place_id')
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
 #/find_place/?date_start=2023-10-01&date_end=2023-11-13
@csrf_exempt
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def find_place_by_dates(request):
    date_start = datetime.strptime(request.GET.get('date_start'), '%Y-%m-%d')
    date_end = datetime.strptime(request.GET.get('date_end'), '%Y-%m-%d')
    return JsonResponse({"Message": find_avalivable_place(date_start, date_end)})

def find_avalivable_place(date_start, date_end):
    places = list(Factory_Place.objects.all().values_list())
    places = list(map(lambda place: place[0], places))
    reservation = list(Reserve_Factory.objects.all().values_list())
    reservation_correct = list(filter(lambda place:(((place[2].replace(tzinfo = None) > date_start < place[3].replace(tzinfo = None)) and (place[2].replace(tzinfo = None) > date_end < place[3].replace(tzinfo = None  )))), reservation))
    reservation_correct2 = list(filter(lambda place:(((place[2].replace(tzinfo = None) < date_start > place[3].replace(tzinfo = None)) and (place[2].replace(tzinfo = None) < date_end > place[3].replace(tzinfo = None)))),reservation))
    reservation_correct = reservation_correct + reservation_correct2
    reservation_correct = list(map(lambda place: place[1], reservation_correct))
    if(reservation_correct == []):
        reservation = list(Reserve_Factory.objects.all().values_list())
        reservation = list(map(lambda place: place[1], reservation))
        available_places = list(filter (lambda place: place not in reservation, places))
    else:
        available_places = list(set(places + reservation_correct))
    if(available_places != []):
        return available_places
    else:
        return "No hay lugares disponibles en esa fecha"
        
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def cancel_reservation(request):
    id_reserve = request.GET.get('id_reserve')
    try:
        Reserve_Factory.objects.get(id = id_reserve)
        reserve.delete()
        return JsonResponse({"message": "Reserva cancelada correctamente"})
    except:
        return JsonResponse({"message": "No existe la reserva"})
 
def verify_dates(date_start, date_end, date_start_reservation, date_end_reservation):
    return verify_before_dates(date_start, date_end, date_start_reservation) and verify_after_dates(date_start, date_end, date_end_reservation)
    
def verify_after_dates(start, end, date):
    return start > date < end

def verify_before_dates(start, end, date):
    return start < date > end 