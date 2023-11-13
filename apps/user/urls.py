from rest_framework.routers import DefaultRouter
from apps.user import views

user_router = DefaultRouter()
user_router.register('users', views.UserViewSet)
