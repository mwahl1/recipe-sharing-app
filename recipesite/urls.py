
#URL configuration for recipesite project.
#
#The `urlpatterns` list routes URLs to views. For more information please see:
#    https://docs.djangoproject.com/en/5.1/topics/http/urls/
#Examples:
#Function views
#    1. Add an import:  from my_app import views
#    2. Add a URL to urlpatterns:  path('', views.home, name='home')
#Class-based views
#    1. Add an import:  from other_app.views import Home
#    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
#Including another URLconf
#    1. Import the include() function: from django.urls import include, path
#    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))


# recipesite/urls.py
from django.conf import settings
from django.conf.urls.static import static
from recipes.views import SignUpView

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.home, name='home'),  # Remove or comment out this line
    path('', include('recipes.urls')),    # Direct root URL to recipes app
]



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('recipes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
