from cmath import inf, pi
from datetime import datetime, tzinfo
from django.shortcuts import render
import json
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
<<<<<<< HEAD
from .models import *
=======
from .models import Factory_Place, Material, Material_Provider, Material_arrived, Reserve_Factory
>>>>>>> main
import jwt
from rest_framework_swagger.views import get_swagger_view

@csrf_exempt
def login(request):
    body = json.loads(request.body)
    print(body.get('username'))
    token = jwt.encode({"username": body.get('username'), "exp":1371720939}, algorithm='HS256', key='secret')
    print(token)
 
# Query para probar el método 
# localhost:8000/ask_for_material/?id_material=4&date_expected=2022-11-19&cantidad=100   
@api_view(['GET'])
def ask_for_material(request):
    id_material = request.GET.get('id_material')
    date_expected = request.GET.get('date_expected')
    cantidad = request.GET.get('cantidad')
    return JsonResponse({"materials": get_providers_for_material(id_material, date_expected, cantidad)})

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
<<<<<<< HEAD

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
        sede = Factory_place.objects.get(id=id_sede)
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
=======
    
@csrf_exempt
@api_view(['POST'])
def reserve(request):
    request_body = json.loads(request.body)
    
    Reserve_Factory.objects.create(factory_place_id = request_body.get('factory_place_id'), date_start = request_body.get('date_start'), date_end = request_body.get('date_end'), enterprise = request_body.get('enterprise'), state = request_body.get('state'))
    return JsonResponse({"message": "Reserva creada exitosamente"})

@csrf_exempt
@api_view(['GET'])
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
>>>>>>> main
