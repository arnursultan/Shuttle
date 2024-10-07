from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .users.views import (RegistrationViewSet, RatingViewSet,
                          DriverViewSet, CreatePaymentIntentView,
                          ConfirmPaymentView, CustomTokenObtainPairView,
                          TwoFactorAuthViewSet)

router = DefaultRouter()
router.register(r'registration', RegistrationViewSet, basename='registration')
router.register(r'rating', RatingViewSet, basename='rating')
router.register(r'driver', DriverViewSet, basename='driver')
router.register(r'2fa', TwoFactorAuthViewSet, basename='twofactor')

urlpatterns = [
    path('', include(router.urls)),
    path('create-payment-intent/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
    path('confirm-payment/', ConfirmPaymentView.as_view(), name='confirm-payment'),
    path('login/', CustomTokenObtainPairView.as_view(), name='api_login'),
    path('refresh/', TokenRefreshView.as_view(), name='api_refresh'),
]
w