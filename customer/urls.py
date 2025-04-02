from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import CustomerViewSet, LoginView, RegisterView, signup_view, login_view, activate_account

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')

urlpatterns = [
    path('', include(router.urls)),

    # API authentication
    path('register/', RegisterView.as_view(), name='api_register'),
    path('login/', LoginView.as_view(), name='api_login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Frontend authentication
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),
]
