from rest_framework import serializers

from orders.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = (
            "product",
            "quantity",
            "price",
        )


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "first_name",
            "last_name",
            "email",
            "address",
            "zipcode",
            "place",
            "phone",
            "paid_amount",
            "payment_token",
            "paid",
            "delivered",
            "cash_on_delivery",
            "items",
            "created_by",
            "created_at",
            "modified_at",
        )
        read_only_fields = ("payment_token", "created_by", "created_at", "modified_at",)

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for items_data in items_data:
            OrderItem.objects.create(order=order, **items_data)
        return order
