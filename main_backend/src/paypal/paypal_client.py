import base64
import datetime
import requests
from django.conf import settings
import json


class PayPalClient:
    """
    A paypal client that calls the PayPal RESTful API to accept payments
    """
    access_token = ''
    token_expire = ''
    app_id = ''
    mode = ''

    def __init__(self, mode, client_id, client_secret):
        self.mode = mode
        self.client_id = client_id
        self.client_secret = client_secret

    @property
    def base_url(self):
        """
        Set the base url depends on the mode
        """
        if self.mode == 'sandbox':
            return "https://api.sandbox.paypal.com"
        elif self.mode == 'real':
            return "https://api.paypal.com"
        else:
            raise ValueError("The mode should be 'real' or sandbox")

    def generate_access_token(self):
        """
        Generate the access token that is used to access the API
        """
        url = f"{self.base_url}/v1/oauth2/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic {0}".format(base64.b64encode((self.client_id + ":" + self.client_secret)
                                                                 .encode()).decode())
        }
        response = requests.post(url, data, headers=headers).json()
        self.access_token = response.get('access_token')
        return response.get('access_token')

    def create_order(self, total_amount, currency_code='USD',
                     return_url='https://127.0.0.1', cancel_url='https://127.0.0.1',
                     ):
        """
        Create order by taking some arguments
        total_amount -> the total of purchase that customer should pay
        currency_code -> the code for the currency that user should pay with (USD, EUR, EG, SAR)
        return_url -> the url that user redirected to it after the payment is successfully done
        cancel_url -> the url that user redirected to it when the payment is canceled
        RETURN:
            A Json response with some API urls
        """
        if not self.access_token:
            self.generate_access_token()
        headers = {"Content-Type": "application/json", "Authorization": f'Bearer {self.access_token}'}
        url = f"{self.base_url}/v2/checkout/orders"
        data = {
                "intent": "CAPTURE",
                "application_context": {
                    "return_url": return_url,
                    "cancel_url": cancel_url,
                    "brand_name": "Ecommerce INC",
                    "landing_page": "BILLING",
                    "user_action": "PAY_NOW"
                },
                "purchase_units": [
                    {
                        "amount": {
                            "currency_code": currency_code,
                            "value": f"{float(total_amount):02}",
                        }
                    }
                ]
            }
        result = requests.post(url=url, data=json.dumps(data), headers=headers).json()
        return result

    def capture_payment(self, order_id):
        """
        check if the payment has been done or no and capture it in the business account
        Arguments:
            order_id -> the order that we want to capture its payment.
        """
        if not self.access_token:
            self.generate_access_token()
        headers = {"Content-Type": "application/json", "Authorization": f'Bearer {self.access_token}'}
        url = f"{self.base_url}/v2/checkout/orders/{order_id}/capture"
        data = {"intent": "CAPTURE"}

        result = requests.post(url=url, data=json.dumps(data), headers=headers).json()
        return result
