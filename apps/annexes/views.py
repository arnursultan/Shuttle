from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.annexes.models import Certificate, Application, Building, Driver, Route, Category, Review, Profile, Car
from apps.annexes.serializers import CertificateSerializer, ApplicationSerializer, BuildingSerializer, DriverSerializer, \
    CategorySerializers, ReviewSerializers, ProfileSerializer, CarSerializer, RouteSerializer


class CategoryAPIViews(GenericViewSet,
                       mixins.CreateModelMixin,
                       mixins.ListModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers


class ReviewAPIViews(GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers


class CertificateViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer


class ApplicationViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer


class BuildingViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer

    @action(detail=False, methods=['get'])
    def catalog(self, request):
        buildings = self.get_queryset()
        serializer = self.get_serializer(buildings, many=True)
        return Response(serializer.data)


class DriverViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.wallet_balance < 0:
            return Response({"detail": "Negative wallet balance is not allowed."}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if request.data.get('wallet_balance', 0) < 0:
            return Response({"detail": "Negative wallet balance is not allowed."}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)


class CarViewSet(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class ProfileViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class RouteViewSet(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer