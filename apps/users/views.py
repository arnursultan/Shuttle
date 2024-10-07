import stripe
from rest_framework.viewsets import GenericViewSet, ViewSet
from rest_framework import mixins, views, status, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
from random import randint
from datetime import timedelta
from django.utils import timezone
from .users.models import (Rating, Driver,
                           Registration,
                           LoginCode)
from .users.serializers import (RatingSerializer,
                                DriverSerializer,
                                RegistrationSerializer,
                                TwoFactorAuthSerializer)


class RegistrationViewSet(GenericViewSet,
                          mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.ListModelMixin):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer


class RatingViewSet(GenericViewSet,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class DriverViewSet(GenericViewSet,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer


class CreatePaymentIntentView(views.APIView):
    def post(self, request, *args, **kwargs):
        try:
            amount = request.data.get('amount')
            currency = request.data.get('currency', 'usd')

            intent = stripe.PaymentIntent.create(
                amount=int(amount),
                currency=currency,
            )

            return Response({
                'client_secret': intent.client_secret,
                'publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ConfirmPaymentView(views.APIView):
    def post(self, request, *args, **kwargs):
        try:
            payment_intent_id = request.data.get('payment_intent_id')

            intent = stripe.PaymentIntent.confirm(payment_intent_id)

            if intent.status == 'succeeded':
                return Response({'detail': 'Payment succeeded!'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': f'Payment failed with status {intent.status}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user_id = user.id
        response.data['user_id'] = user_id
        return response


class TwoFactorAuthViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = TwoFactorAuthSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Authentication has been successful"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        return Response({"message": "This method is unsupported"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
