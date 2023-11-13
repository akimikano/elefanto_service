from rest_framework import viewsets
from rest_framework import mixins
from apps.common.constants import ExceptionText
from apps.common.exceptions import UserException
from apps.common.exceptions import AuthException
from apps.user.models import User
from apps.user.serializers import UserCreateSerializer
from apps.user.serializers import UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework.permissions import AllowAny
from django.conf import settings
from apps.user.services import send_activation_email
from apps.user.services import activate_user
from rest_framework_simplejwt.exceptions import TokenError
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from drf_yasg import openapi


@method_decorator(name='create', decorator=swagger_auto_schema(
    responses={'200': UserSerializer()}
))
class UserViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = AllowAny,

    def get_serializer_class(self):
        serializers_map = {
            'create': UserCreateSerializer,
            'jwt_create': TokenObtainPairSerializer,
            'jwt_refresh': TokenRefreshSerializer,
            'jwt_verify': TokenVerifySerializer
        }
        return serializers_map.get(self.action, self.serializer_class)

    def perform_create(self, serializer):
        user = serializer.save()
        if settings.SEND_ACTIVATION_EMAIL:
            send_activation_email(user)

    @swagger_auto_schema(
        responses={'200': '{"success": true}'},
        manual_parameters=[
            openapi.Parameter('token', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True)
        ]
    )
    @action(['get'], True)
    def activate(self, request, pk):
        user = self.get_object()
        if activate_user(user, request.GET.get('token')):
            return Response({'success': True})
        raise UserException(ExceptionText.INVALID_ACTIVATION_TOKEN)

    @swagger_auto_schema(responses={'200': TokenRefreshSerializer()})
    @action(['post'], False)
    def jwt_create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)

    @action(['post'], False)
    def jwt_refresh(self, request):
        serializer = self.get_serializer(data=request.data)
        self.handle_token_error(serializer)
        return Response(serializer.data)

    @swagger_auto_schema(responses={'200': '{}'})
    @action(['post'], False)
    def jwt_verify(self, request):
        serializer = self.get_serializer(data=request.data)
        self.handle_token_error(serializer)
        return Response(serializer.data)

    @staticmethod
    def handle_token_error(serializer):
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise AuthException(e.args[0])
