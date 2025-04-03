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
from django.shortcuts import render, redirect
from django.contrib import messages

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
                 f"http://{current_site.domain}/activate/{urlsafe_base64_encode(force_bytes(user.pk))}/{generate_token.make_token(user)}/",  
            from_email=settings.EMAIL_HOST_USER,  
            to=[user.email]
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

# Frontend views
def signup_view(request):
    if request.method == 'POST':
        # Handle form submission
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        country = request.POST.get('country')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, "Passwords don't match")
            return redirect('signup')
        
        # Check if user already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('signup')
        
        if Customer.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "Phone number already exists")
            return redirect('signup')
        
        try:
            # Create user with authentication info
            user = CustomUser.objects.create_user(
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            user.is_active = False
            user.save()

            # Create customer profile with business info
            customer = Customer.objects.create(
                user=user,
                phone_number=phone_number,
                country=country
            )
            
            try:
                # Send activation email
                current_site = get_current_site(request)
                email_message = EmailMessage(
                    subject='Confirm your email @ Dexmiq_Tourism!',
                    body=f"Hello {user.first_name},\n\nClick the link below to verify your email:\n\n"
                         f"http://{current_site.domain}/activate/{urlsafe_base64_encode(force_bytes(user.pk))}/{generate_token.make_token(user)}/",
                    from_email=settings.EMAIL_HOST_USER,
                    to=[user.email]
                )
                email_message.send()
                messages.success(request, "Registration successful. Please check your email to activate your account.")
            except Exception as e:
                # If email fails, still create the account but inform the user
                user.is_active = True  # Activate the user anyway
                user.save()
                messages.warning(request, "Account created successfully, but we couldn't send the activation email. You can log in now.")
            
            return redirect('login')
            
        except Exception as e:
            messages.error(request, "An error occurred during registration. Please try again.")
            return redirect('signup')
    
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Get user by email
        try:
            user = CustomUser.objects.get(email=email)
            # Authenticate with username (which is email in this case)
            user = authenticate(username=user.username, password=password)
        except CustomUser.DoesNotExist:
            user = None
        
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('homepage')
            else:
                messages.error(request, "Your account is not activated. Please check your email for activation link.")
                return redirect('login')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('login')
    
    return render(request, 'login.html')

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated. You can now login.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid or has expired.")
        return redirect('signup')

def profile_view(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please login to view your profile.")
        return redirect('login')
    
    try:
        # Get the customer profile and their bookings
        customer = request.user.customer_profile
        bookings = customer.bookings.all().order_by('-booking_date')
    except Customer.DoesNotExist:
        # For admin users or users without customer profile
        bookings = []
    
    context = {
        'user': request.user,
        'bookings': bookings,
        'booking_count': len(bookings)
    }
    
    return render(request, 'profile.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('homepage')