from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Plant, Disease, Treatment
from .serializers import PlantSerializer
from rest_framework.permissions import IsAuthenticated



# 🔹 BULK ADD API
@api_view(['POST'])
def bulk_add_data(request):
    data_list = request.data

    if not isinstance(data_list, list):
        return Response({"error": "Expected a list of data"}, status=400)

    for data in data_list:
        plant, _ = Plant.objects.get_or_create(name=data.get('plant'))

        disease = Disease.objects.create(
            plant=plant,
            name=data.get('disease'),
            description=data.get('description'),
            symptoms=data.get('symptoms'),
            causes=data.get('causes')
        )

        Treatment.objects.create(
            disease=disease,
            medicines=data.get('medicines'),
            dosage=data.get('dosage'),
            precautions=data.get('precautions'),
            organic_alternatives=data.get('organic')
        )

    return Response({"message": "Bulk data added successfully ✅"})


# 🔹 GET PLANTS API (WITH SEARCH)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def plant_list_api(request):
    query = request.GET.get('q')
    symptom = request.GET.get('symptom')
    disease_name = request.GET.get('disease')

    plants = Plant.objects.all()

    # 🔍 Search by plant name
    if query:
        plants = plants.filter(name__icontains=query)

    # 🌿 Filter by symptoms
    if symptom:
        plants = plants.filter(
            diseases__symptoms__icontains=symptom
        ).distinct()

    # 🌾 Filter by disease name
    if disease_name:
        plants = plants.filter(
            diseases__name__icontains=disease_name
        ).distinct()

    # ❌ No result handling
    if not plants.exists():
        return Response({
            "message": "No plant found ❌",
            "data": []
        })

    serializer = PlantSerializer(plants, many=True)
    return Response(serializer.data)


# 🔹 FRONTEND VIEW
def home(request):
    plants = Plant.objects.all()
    diseases = None
    selected_plant = None

    # 🔍 SEARCH
    query = request.GET.get('q')
    if query:
        plants = plants.filter(name__icontains=query)

    # 🌿 SELECT PLANT
    plant_id = request.GET.get('plant')
    if plant_id:
        try:
            selected_plant = Plant.objects.get(id=plant_id)
            diseases = selected_plant.diseases.all()
        except Plant.DoesNotExist:
            selected_plant = None
            diseases = None

    return render(request, 'home.html', {
        'plants': plants,
        'diseases': diseases,
        'selected_plant': selected_plant
    })