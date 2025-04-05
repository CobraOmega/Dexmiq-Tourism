import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from booking.models import Booking
from . models import Payment
from decimal import Decimal
import math

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request, id):
    try:
        booking = get_object_or_404(Booking, id = id)  #booking details

        # Check if total_price is valid
        if booking.total_price is None or math.isinf(booking.total_price) or math.isnan(booking.total_price):
            # Handle invalid total_price
            return render(request, "error.html", {"message": "Invalid booking price. Please contact support."})
        
        # Set a maximum price to avoid potential issues
        safe_price = min(booking.total_price, 999999.99)
        
        # Convert float to Decimal for the payment model
        amount_as_decimal = Decimal(str(safe_price))

        # For payment status == pending & to check is a payment is created
        payment, created = Payment.objects.get_or_create(
            booking=booking,
            defaults={
                "user": request.user,
                "amount": amount_as_decimal,
                "status": "pending",
            }
        )

        session = stripe.checkout.Session.create(
            payment_method_types = ['card'],
            line_items = [{
                'price_data': {
                    'currency' : 'inr',
                    'product_data' : {'name': booking.package.title},
                    'unit_amount' : int(safe_price * 100),     #stripe stores amount in paisa (1 rupee == 100 paisa)
                },
                'quantity': 1,
            }],
            mode = 'payment',
            success_url = f'http://127.0.0.1:8000/payment/success/{payment.payment_id}/',
            cancel_url = f'http://127.0.0.1:8000/payment/failed/{payment.payment_id}/'
        )
        return redirect(session.url)
    
    except Booking.DoesNotExist:
        return render(request, "error.html", {"message": "Booking does not exist"})
    except Exception as e:
        # Catch any other errors
        return render(request, "error.html", {"message": f"Payment processing error: {str(e)}"})
    
def payment_success(request, payment_id):
    try:
        payment = Payment.objects.get(payment_id = payment_id)

        payment.status = 'paid'
        payment.save()
        
        # Update booking status to confirmed after payment
        booking = payment.booking
        booking.status = 'confirmed'
        booking.save()

        return render(request, "payment/success.html", {"payment": payment})

    except Payment.DoesNotExist:
        return render(request, "error.html", {"message": "Payment not found"})
    
def payment_failed(request, payment_id):
    try:
        payment = Payment.objects.get(payment_id = payment_id)      #Get payment record

        payment.status = 'failed'
        payment.save()

        return render(request, "failed.html", {"payment": payment})
    
    
    except Payment.DoesNotExist:
        return render(request, "error.html", {"message": "Payment not found"})