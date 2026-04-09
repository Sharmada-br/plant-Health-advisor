from django.shortcuts import render
from .models import Plant, Disease
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Plant
from .serializers import PlantSerializer


@api_view(['GET'])
def plant_list_api(request):
    plants = Plant.objects.all()
    serializer = PlantSerializer(plants, many=True)
    return Response(serializer.data)

def home(request):
    plants = Plant.objects.all()
    diseases = None
    selected_plant = None

    # 🔍 SEARCH
    query = request.GET.get('q')
    if query:
        plants = plants.filter(name__icontains=query)
        diseases = Disease.objects.filter(name__icontains=query)

    # 🌿 SELECT PLANT
    if request.method == 'POST':
        plant_id = request.POST.get('plant')
        if plant_id:
            try:
                selected_plant = Plant.objects.get(id=plant_id)
                diseases = selected_plant.diseases.all()
            except:
                diseases = None

    return render(request, 'home.html', {
        'plants': plants,
        'diseases': diseases,
        'selected_plant': selected_plant
    })