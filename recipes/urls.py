# recipes/urls.py

# recipes/urls.py

from django.contrib import admin
from django.urls import path, include
from recipes import views

urlpatterns = [
    path('', views.RecipeListView.as_view(), name='recipe-list'),
    path('<int:pk>/', views.RecipeDetailView.as_view(), name='recipe-detail'),
    path('add/', views.RecipeCreateView.as_view(), name='recipe-add'),
]


urlpatterns = [
    path('', views.RecipeListView.as_view(), name='recipe-list'),
    path('recipe/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe-detail'),
    path('recipe/new/', views.RecipeCreateView.as_view(), name='recipe-create'),
    path('recipe/<int:pk>/edit/', views.RecipeUpdateView.as_view(), name='recipe-update'),
    path('recipe/<int:pk>/delete/', views.RecipeDeleteView.as_view(), name='recipe-delete'),
    path('recipe/<int:pk>/favorite/', views.add_favorite, name='add-favorite'),
    path('recipe/<int:pk>/unfavorite/', views.remove_favorite, name='remove-favorite'),
    path('recipe/<int:pk>/review/', views.add_review, name='add-review'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]

