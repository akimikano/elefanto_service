from rest_framework import viewsets
from rest_framework import mixins
from apps.book.filters import BookFilter
from apps.book.models import Book, Rate
from apps.book.serializers import BookListSerializer
from apps.book.serializers import BookDetailSerializer
from apps.book.serializers import RateCreateSerializer
from django.db.models import Avg
from django.db.models import Exists
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.utils import no_body


class BookViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    filterset_class = BookFilter

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == 'retrieve':
            qs = qs.prefetch_related(
                'authors', 'genres', 'rate_set__user'
            ).annotate(
                average_rating=Avg('rate__rate')
            ).annotate(
                is_saved=Exists(self.request.user.saved_books.all())
            )
        return qs

    def get_serializer_class(self):
        serializers_map = {
            'list': BookListSerializer,
            'retrieve': BookDetailSerializer
        }
        return serializers_map.get(self.action, self.serializer_class)

    @swagger_auto_schema(request_body=no_body,
                         responses={'200': '{"success": true}'})
    @action(['post'], True)
    def save(self, request, pk):
        book = self.get_object()
        request.user.saved_books.add(book)
        return Response({'success': True})

    @swagger_auto_schema(request_body=no_body,
                         responses={'200': '{"success": true}'})
    @action(['post'], True)
    def unsave(self, request, pk):
        book = self.get_object()
        request.user.saved_books.remove(book)
        return Response({'success': True})


class RateViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin):
    queryset = Rate.objects.all()
    serializer_class = RateCreateSerializer
