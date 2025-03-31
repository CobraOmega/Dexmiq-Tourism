from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import logout, authenticate, login, get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage  
from dexmiq_tourism import settings
from customer.models import Customer
from .models import CustomUser
from .serializers import CustomerSerializer, RegisterSerializer, LoginSerializer
from .tokens import generate_token

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

# Register API
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()

            # Email Verification
            current_site = get_current_site(request)
            email = EmailMessage(
            subject='Confirm your email @ Dexmiq_Tourism!',  
            body = f"Hello {user.first_name},\n\nClick the link below to verify your email:\n\n" \
                 f"http://{current_site.domain}/api/auth/activate/{urlsafe_base64_encode(force_bytes(user.pk))}/{generate_token.make_token(user)}/",  
            from_email=settings.EMAIL_HOST_USER,  
            to=[user.email]  # ✅ Ensure `to` is a list
        )
            email.send()

            return Response({"message": "User registered successfully. Check your email for activation."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Login API
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data = request.data)

        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# Logout API
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_logout(request):
    logout(request)
    return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)


# Email Verification
class ActivateAccount(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return Response({"error": "Invalid activation link"}, status=status.HTTP_400_BAD_REQUEST)

        if generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Account activated successfully"}, status=status.HTTP_200_OK)

        return Response({"error": "Activation failed"}, status=status.HTTP_400_BAD_REQUEST)


# Protected API 
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "This is a protected route"}, status=status.HTTP_200_OK)