from rest_framework import serializers
from apps.book.models import Book
from apps.book.models import Author
from apps.book.models import Rate
from apps.book.models import Genre
from apps.common.constants import seo_fields
from apps.user.serializers import UserSerializer
from drf_yasg.utils import swagger_serializer_method


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class RateListSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Rate
        fields = ('id', 'user', 'rate', 'text')


class RateCreateSerializer(serializers.ModelSerializer):
    rate = serializers.IntegerField(min_value=0, max_value=5)

    class Meta:
        model = Rate
        fields = ('id', 'book', 'rate', 'text')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'name')


class BookDetailSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    authors = AuthorSerializer(many=True)
    rates = RateListSerializer(many=True, source='rate_set')
    average_rating = serializers.SerializerMethodField()
    is_saved = serializers.BooleanField()

    class Meta:
        model = Book
        fields = seo_fields + [
            'id', 'name', 'description', 'published_date', 'genres', 'authors',
            'rates', 'average_rating', 'is_saved'
        ]

    @swagger_serializer_method(serializers.FloatField())
    def get_average_rating(self, instance):
        rating = instance.average_rating or 0
        return round(rating, 1)
