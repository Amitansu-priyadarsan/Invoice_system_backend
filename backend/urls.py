from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from invoices import views

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'invoices', views.InvoiceViewSet, basename='invoice')
router.register(r'invoices/(?P<id>\d+)', views.InvoiceDetail, basename='invoice-detail')  # Register InvoiceDetail as a ViewSet with a dynamic URL

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Include the router's URL patterns
]
