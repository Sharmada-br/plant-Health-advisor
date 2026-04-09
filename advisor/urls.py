from django.urls import path
from . import views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Plant
from .serializers import PlantSerializer

@api_view(['GET'])
def plant_api(request):
    plants = Plant.objects.all()
    serializer = PlantSerializer(plants, many=True)
    return Response(serializer.data)

urlpatterns = [
    path('', views.home, name='home'),
    path('api/plants/', plant_api),
]