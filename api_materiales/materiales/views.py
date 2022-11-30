from cmath import inf, pi
from datetime import date, datetime, tzinfo
import json
from django.views.decorators.csrf import csrf_exempt
from .models import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from .serializers import *
from rest_framework.response import Response
from rest_framework import status


class ProviderViewSet(viewsets.ModelViewSet):
   queryset = Provider.objects.all()
   serializer_class = ProviderSerializer


# Query para probar el método 
# localhost:8000/ask_for_material/?id_material=4&date_expected=2022-11-19&cantidad=100   
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def ask_for_material(request):
    id_material = request.GET.get('id_material')
    date_expected = request.GET.get('date_expected')
    cantidad = request.GET.get('cantidad')
    providers = get_providers_for_material(id_material, date_expected, cantidad)
    if (isinstance(providers, list)):
        serializer = ProviderSerializer(providers, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response('Error en la consulta', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def materials(request):
    materials = Material.objects.all()
    serializer = MaterialSerializer(materials, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def enterprises(request):
    enterprises = Enterprise.objects.all()
    serializer = EnterpriseSerializer(enterprises, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def providers(request):
    providers = Provider.objects.all()
    serializer = ProviderSerializer(providers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def material_provider(request):
    material_provider = Material_Provider.objects.all()
    serializer = MaterialProviderSerializer(material_provider, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def material_reservations(request):
    coleccion = request.GET.get('coleccion')
    reservations = Material_reservation.objects.filter(coleccion = int(coleccion))
    serializer = MaterialReservationSerializer(reservations, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def place_reservations(request):
    coleccion = request.GET.get('collection')
    reservations = Place_reservation.objects.filter(coleccion = int(coleccion))
    serializer = PlaceReservationSerializer(reservations, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)

def get_providers_for_material(id_material, date_expected, cantidad):
    providers_list = []
    try:
        providers_for_material =  Material_Provider.objects.all().filter(material_id = int(id_material)).values_list()
        for provider in list(providers_for_material):
            if( provider[3] >= int(cantidad)):
                provider= Provider.objects.get(id=int(provider[2]))
                providers_list.append(provider)
            else:
                if((compromised_materials_for_provider(provider[2], date_expected, id_material) + provider[3]) > int(cantidad)):
                    provider= Provider.objects.get(id=int(provider[2]))
                    providers_list.append(provider)
    except Exception as err: 
        print(err)
    return providers_list

def compromised_materials_for_provider(id_provider,expected_date, id_material):
    expected_date = datetime.strptime(expected_date, '%Y-%m-%d')
    materials = Material_arrived.objects.all().filter(provider_id = int(id_provider), material_id = int(id_material)).values_list()
    materials_in_date = filter(lambda material: datetime.now()<= material[4].replace(tzinfo = None) <= expected_date, materials)
    return sum(map(lambda material: material[3], materials_in_date))

@csrf_exempt
@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def stock_update(request):
    body = json.loads(request.body)
    material_id = body.get('material_id')
    provider_id = body.get('provider_id')
    amount = body.get('amount')
    try:
        material_provider = Material_Provider.objects.get(material_id = int(material_id), provider_id = int(provider_id))
    except Material_Provider.DoesNotExist:
        return Response("No existe el material indicado para dicho proveedor", status=status.HTTP_404_NOT_FOUND)
    else:
        updated_amount = material_provider.total_amount + int(amount)
        material_provider.update_stock(updated_amount)
        serializer = MaterialProviderSerializer(material_provider)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
    request_body = json.loads(request.body)
    id_material = request_body.get("id_material")
    id_provider = request_body.get("id_provider")
    amount = request_body.get("amount")
    reserve_date = request_body.get("reserve_date")
    id_sede = request_body.get("id_sede")
    id_coleccion = request_body.get("id_coleccion")
    new_reserve = reserve_material_of_provider(id_material, id_provider, amount, reserve_date, id_sede, id_coleccion)
    if(isinstance(new_reserve, str)):
        return Response(new_reserve, status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer = MaterialReservationSerializer(new_reserve)
        return Response(serializer.data, status=status.HTTP_200_OK)

def reserve_material_of_provider(id_material, id_provider, amount, reserve_date, id_sede, id_coleccion):
    try:
        material_provider = Material_Provider.objects.all().filter(material_id=id_material, provider_id=id_provider)[0]
        material_provider.compromise_amount = material_provider.compromise_amount + int(amount)
        material_provider.save()
        material = Material.objects.get(id=id_material)
        provider = Provider.objects.get(id=id_provider)
        sede = Factory_Place.objects.get(id=id_sede)
        coleccion = int(id_coleccion)
        newReserve = Material_reservation.objects.create(material=material, provider=provider, amount=amount, reserve_date=reserve_date, place=sede, state='active', coleccion=coleccion)
    except IndexError:
        return "No existe el material indicado para dicho proveedor"
    except: 
        return "Error en la consulta"
    return newReserve

test_param = openapi.Parameter('test', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_BOOLEAN)

@swagger_auto_schema(method='get', manual_parameters=[test_param])
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def update_material_reservation(request):
    id_reserve = request.GET.get('id_reserve')
    state = request.GET.get('state')
    try:
        reserve = Material_reservation.objects.get(id=id_reserve)
        if(state == 'cancelled'):
            material_provider = Material_Provider.objects.all().filter(material_id=reserve.material, provider_id=reserve.provider)[0]
            material_provider.compromise_amount = material_provider.compromise_amount - reserve.amount
            material_provider.save()
        reserve.state = state
        reserve.save(update_fields=['state'])
    except IndexError:
        return Response("No existe el material indicado para dicho proveedor", status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response("No existe la reserva indicada", status=status.HTTP_400_BAD_REQUEST)
    return Response("Reserva actualizada correctamente", status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def reserve_place(request):
    request_body = json.loads(request.body)
    date_start = datetime.strptime(request_body.get('date_start'), '%Y-%m-%d')
    date_end = datetime.strptime(request_body.get('date_end'), '%Y-%m-%d')
    factory_place_id = request_body.get('factory_place_id')
    coleccion = request_body.get('coleccion_id')
    available_spaces = find_available_place(date_start,date_end)
    if (isinstance(available_spaces, str)):
        return Response(available_spaces, status=status.HTTP_404_NOT_FOUND)
    else:
        if(int(factory_place_id) not in available_spaces):
            return Response("No hay lugares disponibles en esa fecha", status=status.HTTP_404_NOT_FOUND)
        else:
            factory = Factory_Place.objects.get(id = request_body.get('factory_place_id'))
            reserve = Place_reservation.objects.create(place = factory, date_start = date_start, date_end = date_end, coleccion = int(coleccion), state = "active")
            serializer = PlaceReservationSerializer(reserve)
            return Response(serializer.data, status=status.HTTP_200_OK)

 # /find_place/?date_start=2023-12-9&date_end=2023-12-30
@csrf_exempt
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def find_place_by_dates(request):
    date_start = datetime.strptime(request.GET.get('date_start'), '%Y-%m-%d')
    date_end = datetime.strptime(request.GET.get('date_end'), '%Y-%m-%d')
    places = find_available_place(date_start, date_end)
    if (isinstance(places, str)):
        return Response(places, status=status.HTTP_404_NOT_FOUND)
    else:
        places_objects = Factory_Place.objects.filter(pk__in=places)
        serializer = FactoryPlaceSerializer(places_objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

def find_available_place(date_start, date_end):
    places = list(Factory_Place.objects.all().values_list())
    places = list(map(lambda place: place[0], places))
    reservations = list(Place_reservation.objects.filter(state="active").values_list())
    unavaliable_places = list(filter(lambda place: (place[2].replace(tzinfo = None) <= date_start <= place[3].replace(tzinfo = None) ), reservations))
    unavaliable_places = list(map(lambda place: place[1], unavaliable_places))
    available_places = list(filter(lambda place: place not in unavaliable_places, places))
    if(available_places != []):
        return available_places
    else:
        places_in_date = list(filter(lambda place: date_start >= place[3].replace(tzinfo = None), places))
        if(places_in_date != []):
            return places_in_date
        else:
            return "No hay lugares disponibles en esa fecha"
        
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def update_place_reservation(request):
    id_reserve = request.GET.get('id_reserve')
    state = request.GET.get('state')
    try:
        reserve = Place_reservation.objects.get(id = id_reserve)
        reserve.state = state
        reserve.save(update_fields=['state'])
        return Response("Reserva actualizada correctamente", status=status.HTTP_200_OK)
    except:
        return Response("No existe la reserva indicada", status=status.HTTP_400_BAD_REQUEST)