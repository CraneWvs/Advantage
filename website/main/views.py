from django.http import JsonResponse

from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.serializers import serialize
from datetime import datetime

from .serializers import ZoneSerializer, PlaceSerializer
from .models import Zone, Place


# Create your views here.
# class AdvertiserList(generics.ListAPIView):
#     queryset = models.Advertiser.objects.all()
#     serializer_class = serializers.AdvertiserSerializer

class SolutionsView(TemplateView):
    template_name = "solutions.html"

def zones(request):
    """
    List all zones in form of JsonResponse with Status code 1=DB success, 2=DB fail
    """
    try: 
        zones = serialize('geojson',Zone.objects.all().order_by('-current_impression'))
    except Exception as e:
        return JsonResponse({"status":"2","data":str(e)},status=201)
    return JsonResponse({"status":"1","data":zones},status=201,safe=False)

def zone_detail(request, pk):
    """
    Retrieve detail of a zone
    """
    try:
        zone = Zone.objects.get(pk=pk)
    except Exception as e:
        return JsonResponse({"status":"2","data":str(e)},status=201)

    if request.method == 'GET':
        serializer = ZoneSerializer(zone)
        return JsonResponse({"status":"1","data":serializer.data},status=201)

    # elif request.method == 'PUT':
    #     data = JSONParser().parse(request)
    #     serializer = ZoneSerializer(zone, data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return JsonResponse(serializer.data)
    #     return JsonResponse(serializer.errors, status=400)

def place_in_zone(request, id):
    """
    Retrieve all places of a zone
    """
    try:
        places = serialize('geojson',Place.objects.filter(taxi_zone_id=id,status="Active"))
        # place = Place.objects.filter(taxi_zone_id=id,status="Active")
    except Exception as e:
        return JsonResponse({"status":"2","data":str(e)},status=201)

    if request.method == 'GET':
        return JsonResponse({"status":"1","data":places},status=201,safe=False)
        # serializer = PlaceSerializer(place, many=True)
        # return JsonResponse({"status":"1","data":serializer.data},status=201)
        