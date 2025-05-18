from django.urls import path
from . import views
from .converters import FourDigitYearConverter

app_name = 'portfolio'
urlpatterns = [
    path('', views.portfolio_list, name='portfolio_list'),
    path('create/', views.portfolio_create, name='portfolio_create'),
    path('update/<int:pk>/', views.portfolio_update, name='portfolio_update'),
    path('delete/<int:pk>/', views.portfolio_delete, name='portfolio_delete'),
    path('detail/<slug:slug>/', views.portfolio_detail, name='portfolio_detail'),
    path('archive/<yyyy:year>/', views.archive_by_year, name='archive_by_year'),
    path('category/<slug:cat_slug>/', views.category_detail, name='category_detail'),
    path('tag/<slug:tag_slug>/', views.tag_detail, name='tag_detail'),
]