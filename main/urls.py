from django.urls import path
from .views import AboutView, CategoryView, CreateCategory, SearchView, Nofilterview, NavigationView



urlpatterns = [
    path('navigation/', NavigationView, name='navigation'),
    path('filter/off/', Nofilterview.as_view(), name='nofilter'),
    path('about/', AboutView, name='blog-about'),
    path('category/<str:cats>/', CategoryView, name='cats'),
    path('add/category/', CreateCategory.as_view(), name='createcat'),
    path('search/', SearchView.as_view(), name='search_results'),
]
