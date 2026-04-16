from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse
from difflib import get_close_matches
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Plant, Disease, Treatment
from .serializers import PlantSerializer


# 🔹 BULK ADD API
@api_view(['POST'])
def bulk_add_data(request):
    data_list = request.data

    if not isinstance(data_list, list):
        return Response({"error": "Expected a list of data"}, status=400)

    for data in data_list:
        plant, _ = Plant.objects.get_or_create(name=data.get('plant'))

        disease, created = Disease.objects.get_or_create(
            plant=plant,
            name=data.get('disease'),
            defaults={
                'description': data.get('description'),
                'symptoms': data.get('symptoms'),
                'causes': data.get('causes')
            }
        )

        if created:
            Treatment.objects.create(
                disease=disease,
                medicines=data.get('medicines'),
                dosage=data.get('dosage'),
                precautions=data.get('precautions'),
                organic_alternatives=data.get('organic')
            )

    return Response({"message": "Bulk data added successfully ✅"})


# 🔹 API WITH AUTH
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def plant_list_api(request):
    query = request.GET.get('q')

    plants = Plant.objects.all()

    if query:
        plants = plants.filter(name__icontains=query)

    if not plants.exists():
        return Response({"message": "No plant found ❌", "data": []})

    serializer = PlantSerializer(plants, many=True)
    return Response(serializer.data)


# 🔹 FRONTEND VIEW (SMART + SIMILAR SEARCH)
def home(request):
    plants = Plant.objects.all()
    diseases = None
    selected_plant = None

    query = request.GET.get('q')

    if query:
        plants = Plant.objects.filter(
            Q(name__icontains=query) |
            Q(diseases__name__icontains=query) |
            Q(diseases__symptoms__icontains=query)
        ).distinct()

        # 🔥 SIMILAR SEARCH IF NOTHING FOUND
        if not plants.exists():
            all_names = list(Plant.objects.values_list('name', flat=True))
            similar = get_close_matches(query, all_names, n=5, cutoff=0.5)

            if similar:
                plants = Plant.objects.filter(name__in=similar)

    plant_id = request.GET.get('plant')
    if plant_id:
        try:
            selected_plant = Plant.objects.get(id=plant_id)

            if query:
                diseases = selected_plant.diseases.filter(
                    Q(name__icontains=query) |
                    Q(symptoms__icontains=query)
                ).distinct()
            else:
                diseases = selected_plant.diseases.all()

        except Plant.DoesNotExist:
            selected_plant = None
            diseases = None

    return render(request, 'home.html', {
        'plants': plants,
        'diseases': diseases,
        'selected_plant': selected_plant,
        'query': query 
    })


# 🔹 SEARCH SUGGESTIONS
def search_suggestions(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        plants = Plant.objects.filter(name__icontains=query)[:5]
        for p in plants:
            results.append({"type": "Plant", "name": p.name})

        diseases = Disease.objects.filter(name__icontains=query)[:5]
        for d in diseases:
            results.append({"type": "Disease", "name": d.name})

        symptoms = Disease.objects.filter(symptoms__icontains=query)[:5]
        for s in symptoms:
            results.append({"type": "Symptom", "name": s.symptoms[:40]})

    return JsonResponse(results, safe=False)