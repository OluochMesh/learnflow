from intasend import APIService
from flask import current_app
import json

def create_intasend_checkout(email, amount, plan_name):
    """Initialize IntaSend checkout session"""
    service = APIService(
        public_key=current_app.config['INTASEND_PUBLIC_KEY'],
        secret_key=current_app.config['INTASEND_SECRET_KEY'],
        test=True  # Set to False in production
    )
    checkout = service.checkout.create(
        first_name="LearnFlow",
        last_name="User",
        email=email,
        currency="KES",
        amount=amount,
        comment=plan_name
    )
    return checkout

def verify_webhook_signature(request_data, signature):
    """Verify IntaSend webhook signature"""
    # IntaSend typically sends verification in headers
    # You'll need to implement based on their documentation
    return True  # Implement proper verification