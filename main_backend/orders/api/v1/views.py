import random
import string


from rest_framework import viewsets, status, authentication, permissions
from rest_framework.response import Response

from src.paypal.django_client import get_paypal_client
from orders.models import Order
from orders.api.v1.serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    TODO:set more permissions to allow only super user to see the all orders and payers to see their customers' orders
    """
    lookup_field = "payment_token"
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            paid_amount = sum(
                item.get('quantity') * item.get('product').price for item in serializer.validated_data['items']
            )
            cash_on_delivery = serializer.validated_data["cash_on_delivery"]

            if cash_on_delivery:
                generated_key = 'cash-' + ''.join(random.choice(string.ascii_lowercase) for _ in range(16))
                serializer.save(created_by=request.user, paid_amount=paid_amount, payment_token=generated_key)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            order = get_paypal_client().create_order(paid_amount,
                                                     return_url=request.data.get('return_url', "http://localhost:8080"),
                                                     cancel_url=request.data.get('cancel_url', "http://localhost:8080")
                                                     )
            serializer.save(created_by=request.user, paid_amount=paid_amount, payment_token=order.get('id'))
            return Response(
                {
                    "paypal": [
                        order
                    ],
                    "results": [
                        serializer.data
                    ]
                },
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
