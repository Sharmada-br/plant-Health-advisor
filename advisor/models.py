from django.db import models


class Plant(models.Model):
    name = models.CharField(max_length=100, unique=True)  #  No duplicate plants

    def __str__(self):
        return self.name


class Disease(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='diseases')
    name = models.CharField(max_length=100)
    description = models.TextField()
    symptoms = models.TextField()
    causes = models.TextField()
    image = models.ImageField(upload_to='disease_images/', null=True, blank=True)

    class Meta:
        unique_together = ('plant', 'name')  #  No duplicate disease for same plant

    def __str__(self):
        return f"{self.name} ({self.plant.name})"


class Treatment(models.Model):
    disease = models.OneToOneField(
        Disease,
        on_delete=models.CASCADE,
        related_name='treatment'
    )

    medicines = models.TextField()
    dosage = models.TextField()
    precautions = models.TextField()
    organic_alternatives = models.TextField()

    def __str__(self):
        return f"Treatment for {self.disease.name}"