from rest_framework.routers import DefaultRouter
from apps.book import views

book_router = DefaultRouter()
book_router.register('books', views.BookViewSet)
book_router.register('rate', views.RateViewSet)
