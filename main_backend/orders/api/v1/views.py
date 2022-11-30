import random
import string

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers, vary_on_cookie

from rest_framework import viewsets, status, authentication, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

from src.paypal.django_client import get_paypal_client
from orders.models import Order
from orders.api.v1.serializers import OrderSerializer, MyOrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    TODO:set more permissions to allow only super user to see the all orders and payers to see their customers' orders
    """
    lookup_field = "payment_token"
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.action == "mine":
            return MyOrderSerializer
        return OrderSerializer

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

    @action(methods=["post"], detail=False, name="Capture the payment")
    def capture(self, request):
        if request.user.is_anonymous:
            raise PermissionDenied("You must be logged in to see which Images are yours")
        payment_token = request.data.get('token', None)
        if payment_token:
            order = get_paypal_client().capture_payment(payment_token)
            order_status = order.get('status', None)
            if order_status == 'COMPLETED':
                order = Order.objects.get(payment_token=payment_token)
                order.paid = True
                order.save()
                return Response({"status": "COMPLETED"}, status=status.HTTP_201_CREATED)
            elif order.get('details')[0].get('issue') == 'ORDER_ALREADY_CAPTURED':
                return Response({"status": "ORDER_ALREADY_CAPTURED"}, status=status.HTTP_201_CREATED)
            elif order.get('details')[0].get('issue') == 'ORDER_NOT_APPROVED':
                return Response({"status": "ORDER_NOT_APPROVED"}, status=status.HTTP_201_CREATED)
            elif order.get('details')[0].get('issue') == 'INVALID_RESOURCE_ID':
                return Response({"status": "INVALID_RESOURCE_ID"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"token": "This field is required"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "unknown error has been happened"}, status=status.HTTP_400_BAD_REQUEST)
