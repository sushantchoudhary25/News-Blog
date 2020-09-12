from django.urls import path
from .views import index, blog, post, search


urlpatterns = [
    path('', index, name='index'),
    path('blog/', blog, name='blog'),
    path('post/<id>/', post, name='post'),
    path('search/', search, name='search')
]