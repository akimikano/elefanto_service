from django_filters import rest_framework as filters
from django.db.models import Exists
from django.db.models import OuterRef
from apps.book.models import Book


class BookFilter(filters.FilterSet):
    from_date = filters.DateFilter(method='filter_from_date')
    till_date = filters.DateFilter(method='filter_till_date')

    class Meta:
        model = Book
        fields = ('from_date', 'till_date', 'genres', 'authors')

    def filter_from_date(self, queryset, _, value):
        return queryset.filter(published_date__gte=value)

    def filter_till_date(self, queryset, _, value):
        return queryset.filter(published_date__lte=value)

