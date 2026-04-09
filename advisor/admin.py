from django.contrib import admin
from .models import Plant, Disease, Treatment

admin.site.register(Plant)
admin.site.register(Disease)
admin.site.register(Treatment)