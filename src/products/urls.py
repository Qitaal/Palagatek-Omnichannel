from django.urls import path

from src.products.views import ProductListView, ProductDatatablesJsonView, SynchronizeProduct

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('json', ProductDatatablesJsonView.as_view(), name='product_list_json'),
    path('sync', SynchronizeProduct.as_view(), name='product_sync')
]