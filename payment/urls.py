from django.urls import path
from . import views
from .views import create_checkout_session, payment_failed, payment_success

urlpatterns = [
    path("checkout/<int:id>/", views.create_checkout_session, name='checkout'),
    path("success/<uuid:payment_id>/", payment_success, name='payment_success'),
    path("failed/<uuid:payment_id>/", payment_failed, name='payment_failed'),
]