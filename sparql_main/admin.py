from django.contrib import admin

from .models import Head, Binding, Results, PropertyType

admin.site.register(Head)
admin.site.register(Binding)
admin.site.register(Results)
admin.site.register(PropertyType)

#clean database reset and run the dataset query to see what happens4
# python3 manage.py createsuperuser
# python3 manage.py flush