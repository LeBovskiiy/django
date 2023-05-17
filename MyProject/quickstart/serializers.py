from rest_framework import routers, serializers, viewsets

from users.models import CartItem, CustomUser


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['url', 'username', 'phone', 'email', 'is_staff']


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
