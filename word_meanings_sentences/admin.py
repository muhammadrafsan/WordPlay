from django.contrib import admin
from .models import Makesentence,Score
# Register your models here.
admin.site.register([
    Makesentence,
    Score
])