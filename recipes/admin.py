from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Recipe, Review, Favorite

admin.site.register(Recipe)
admin.site.register(Review)
admin.site.register(Favorite)
