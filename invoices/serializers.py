from rest_framework import serializers
from .models import Invoice, InvoiceDetail


class InvoiceDetailSerializer(serializers.ModelSerializer):
    line_total = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )  # Include line_total as read-only

    class Meta:
        model = InvoiceDetail
        fields = ['description', 'quantity', 'unit_price', 'line_total']
        # 'line_total' is included and read-only, automatically computed on the model


class InvoiceSerializer(serializers.ModelSerializer):
    details = InvoiceDetailSerializer(many=True)
    total_amount = serializers.SerializerMethodField()  # Add total_amount as a computed field

    class Meta:
        model = Invoice
        fields = ['id', 'invoice_number', 'customer_name', 'date', 'details', 'total_amount']

    def get_total_amount(self, obj):
        # Compute the total amount by summing the line_total for all details
        return sum(detail.line_total for detail in obj.details.all())

    def create(self, validated_data):
        details_data = validated_data.pop('details')

        # Create the Invoice object
        invoice = Invoice.objects.create(**validated_data)

        # Add InvoiceDetail objects linked to the newly created Invoice
        for detail_data in details_data:
            InvoiceDetail.objects.create(invoice=invoice, **detail_data)

        return invoice

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details')

        # Update the Invoice object
        instance.invoice_number = validated_data.get('invoice_number', instance.invoice_number)
        instance.customer_name = validated_data.get('customer_name', instance.customer_name)
        instance.date = validated_data.get('date', instance.date)
        instance.save()

        # Delete existing InvoiceDetail objects and create new ones
        instance.details.all().delete()
        for detail_data in details_data:
            InvoiceDetail.objects.create(invoice=instance, **detail_data)

        return instance
