from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination  # Import PageNumberPagination
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Invoice
from .serializers import InvoiceSerializer

# Invoice List and Create View
class InvoiceListCreate(APIView):
    def get(self, request):
        invoices = Invoice.objects.all()
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Print validation errors to the console for debugging
        print("Validation Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InvoicePagination(PageNumberPagination):
    page_size = 5  # Default number of invoices per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class InvoiceViewSet(viewsets.ModelViewSet):
    """
    A viewset for listing, creating, retrieving, updating, and deleting invoices.
    """
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    pagination_class = InvoicePagination

    # Adding filtering, searching, and ordering
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ['invoice_number', 'customer_name', 'date']
    search_fields = ['invoice_number', 'customer_name']
    ordering_fields = ['date', 'invoice_number']
    ordering = ['date']  # Default ordering by date

    def destroy(self, request, *args, **kwargs):
        """
        Override destroy to return a custom response.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Invoice deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)

class InvoiceDetail(viewsets.GenericViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    lookup_field = 'id'  # Specify that the lookup field is 'id'
