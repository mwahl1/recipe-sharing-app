from django.shortcuts import render

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Recipe, Review, Favorite
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
# recipes/views.py

from django.views.generic import ListView
from .models import Recipe

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'  # Specifies the template to use
    context_object_name = 'object_list'        # The default is 'object_list'
    # You can also use 'recipes' or another name if preferred
def home(request):
    return render(request, 'recipes/home.html')  # Ensure this template exists
# class RecipeListView(ListView):
#    model = Recipe
#    template_name = 'recipes/recipe_list.html'
#    context_object_name = 'recipes'
#    paginate_by = 10 

    def get_queryset(self):
        queryset = Recipe.objects.all().order_by('-created_at')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(title__icontains=query) | queryset.filter(description__icontains=query)
        return queryset

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all().order_by('-created_at')
        if self.object.reviews.exists():
            context['average_rating'] = self.object.reviews.aggregate(Avg('rating'))['rating__avg']
        else:
            context['average_rating'] = None
        if self.request.user.is_authenticated:
            context['is_favorited'] = Favorite.objects.filter(user=self.request.user, recipe=self.object).exists()
            context['review_form'] = ReviewForm()
        return context

class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    fields = ['title', 'description', 'ingredients', 'instructions', 'image']
    template_name = 'recipes/recipe_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    fields = ['title', 'description', 'ingredients', 'instructions', 'image']
    template_name = 'recipes/recipe_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author

class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipe-list')
    template_name = 'recipes/recipe_confirm_delete.html'

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.author

@login_required
def add_favorite(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    Favorite.objects.get_or_create(user=request.user, recipe=recipe)
    return redirect('recipe-detail', pk=pk)

@login_required
def remove_favorite(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    Favorite.objects.filter(user=request.user, recipe=recipe).delete()
    return redirect('recipe-detail', pk=pk)

@login_required
def add_review(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.recipe = recipe
            review.save()
            return redirect('recipe-detail', pk=pk)
    else:
        form = ReviewForm()
    return render(request, 'recipes/add_review.html', {'form': form})

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'recipes/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipes'] = self.request.user.recipes.all()
        context['favorites'] = self.request.user.favorites.all()
        return context

