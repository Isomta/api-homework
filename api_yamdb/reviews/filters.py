import django_filters
from django_filters import rest_framework as filters

from .models import Title, Category


class CategoryFilter(django_filters.FilterSet):
    name = filters.CharFilter(
        name='name', lookup_expr='startswith'
    )
    slug = filters.CharFilter()

    class Meta:
        model = Category
        fields = ['name', 'slug']

class TitleFilter(django_filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    category = filters.CharFilter(field_name='category__slug')
    genre = filters.CharFilter(field_name='genre__slug')
    year = filters.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ['name', 'category', 'genre', 'year']



