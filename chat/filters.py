import django_filters
from django_filters import rest_framework as filters

from .models import Message


class UUIDInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class MessageFilter(django_filters.FilterSet):

    before = filters.DateTimeFilter(field_name="updated_at", lookup_expr="lte")
    after = filters.DateTimeFilter(field_name="updated_at", lookup_expr="gte")
    exclude = UUIDInFilter(field_name="id", lookup_expr="in", exclude=True)

    class Meta:
        model = Message
        fields = ["id", "updated_at"]
