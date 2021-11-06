from django_filters import rest_framework as filters

from core.models import User

class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class UserFilter(filters.FilterSet):
    # first_name = CharFilterInFilter(field_name='first_name', lookup_expr='icontains')
    # last_name = CharFilterInFilter(field_name='last_name', lookup_expr='icontains')

    class Meta:
        model = User
        fields = {
            'first_name': ['exact', 'contains'],
            'last_name': ['exact', 'contains'],
            'sex': ['exact'],
        }