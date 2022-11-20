from src.paypal.paypal_client import PayPalClient
from django.conf import settings


def get_paypal_client():
    return PayPalClient(mode=settings.PAYPAL_MODE,
                        client_id=settings.PAYPAL_CLIENT_ID,
                        client_secret=settings.PAYPAL_CLIENT_SECRET
                        )

