from django.urls import path

from src.marketplace.views import MarketplaceListView, ShopeeGenerateAuthLink, AuthShopee

urlpatterns = [
    path('', MarketplaceListView.as_view(), name='marketplace_list'),
    path('get_shopee_auth_link', ShopeeGenerateAuthLink.as_view(), name='get_shopee_auth_link'),
    path('get_shopee_access_token', AuthShopee.as_view(), name='get_shopee_access_token')
]