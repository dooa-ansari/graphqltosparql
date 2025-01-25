from django.db import models

class Head(models.Model):
    vars = models.JSONField()  
    link = models.JSONField()

class Binding(models.Model):
    distribution = models.URLField(null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    mediaType = models.CharField(max_length=255, null=True, blank=True)
    modified = models.DateTimeField(null=True, blank=True)
    identifier = models.CharField(max_length=255, null=True, blank=True)
    accessURL = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    geometry = models.JSONField(null=True, blank=True)
    license = models.URLField(null=True, blank=True)
    publisherName = models.CharField(max_length=255, null=True, blank=True)
    maintainerEmail = models.EmailField(null=True, blank=True)
class Results(models.Model):
    distinct = models.BooleanField(default=False)
    ordered = models.BooleanField(default=False)
    bindings = models.ManyToManyField('Binding', related_name='results')
class Data(models.Model):
    head = models.OneToOneField(Head, on_delete=models.CASCADE)
    results = models.OneToOneField(Results, on_delete=models.CASCADE)
   
