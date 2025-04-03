from django.urls import path
from .views import signup_view, login_view, activate_account, profile_view

urlpatterns = [
    # Frontend authentication
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),
    path('profile/', profile_view, name='profile'),
]
