from django.urls import path
from .views import RegistrationView, VerificationView, LoginView, ActivationView, ProfileView

urlpatterns = [
    path('api/register/', RegistrationView.as_view(), name='user-registration'),
    path('api/verify/', VerificationView.as_view(), name='user-verification'),
    path('api/login/', LoginView.as_view(), name='user-login'),
    path('api/profile/', ProfileView.as_view(), name='user-profile'),
    path('api/activate/', ActivationView.as_view(), name='user-activate'),
]