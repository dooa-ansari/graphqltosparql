from django.db import models

class Head(models.Model):
    vars = models.JSONField()  
    link = models.JSONField()


class PropertyType(models.Model):
    type = models.CharField(max_length=255, null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)
    datatype = models.CharField(max_length=255, null=True, blank=True)
    xmlLang = models.CharField(max_length=255, null=True, blank=True)


class Binding(models.Model):
    distribution = models.OneToOneField(PropertyType, on_delete=models.CASCADE, related_name='distribution_binding')
    title = models.OneToOneField(PropertyType, on_delete=models.CASCADE, related_name='title_binding')
    mediaType = models.OneToOneField(PropertyType, on_delete=models.CASCADE, related_name='mediaType_binding')
    modified = models.OneToOneField(PropertyType, on_delete=models.CASCADE, related_name='modified_binding')
    identifier = models.OneToOneField(PropertyType, on_delete=models.CASCADE, related_name='identifier_binding')
    accessURL = models.OneToOneField(PropertyType, on_delete=models.CASCADE, related_name='accessURL_binding')
    description = models.OneToOneField(PropertyType, on_delete=models.CASCADE, related_name='description_binding')
    geometry = models.OneToOneField(PropertyType, on_delete=models.CASCADE, related_name='geometry_binding')
    license = models.OneToOneField(PropertyType, on_delete=models.CASCADE, related_name='license_binding')
    publisherName = models.OneToOneField(PropertyType, on_delete=models.CASCADE, related_name='publisherName_binding')
    maintainerEmail = models.OneToOneField(PropertyType, on_delete=models.CASCADE, related_name='maintainerEmail_binding')


class Results(models.Model):
    distinct = models.BooleanField(default=False)
    ordered = models.BooleanField(default=False)
    bindings = models.ManyToManyField('Binding', related_name='results')


class Data(models.Model):
    head = models.OneToOneField(Head, on_delete=models.CASCADE)
    results = models.OneToOneField(Results, on_delete=models.CASCADE)
