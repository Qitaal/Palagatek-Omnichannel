import hashlib
import json
import hmac
import requests
import time

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction, DatabaseError
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View

from src.marketplace.models import Marketplaces
from src.products.models import Products, Colors, Variants, ProductsVariantsColors
from src.shared.enum import MarketplaceName
from src.shared.helpers import refresh_shopee_access_token
from django_datatables_view.base_datatable_view import BaseDatatableView


def get_shopee_product_list(shopee, partner_id, partner_key, offset=0):
    shopee = shopee

    timestamp = int(time.time())
    host = settings.LIVE_HOST
    path = "/api/v2/product/get_item_list"
    code = shopee.code
    shop_id = shopee.shop_id
    access_token = shopee.access_token

    tmp_base_string = "%s%s%s%s%s" % (partner_id, path, timestamp, access_token, shop_id)
    base_string = tmp_base_string.encode()

    sign = hmac.new(bytes(partner_key, 'latin-1'), base_string, hashlib.sha256).hexdigest()

    url = host + path + "?access_token=%s&item_status=%s&offset=%s&page_size=%s&partner_id=%s&shop_id=%s&sign=%s&timestamp=%s" % (
        access_token, 'NORMAL', offset, 100, partner_id, shop_id, sign, timestamp)

    resp = requests.get(url)
    return json.loads(resp.content)


def get_shopee_product_list_base_info(shopee, partner_id, partner_key, product_list):
    shopee = shopee

    timestamp = int(time.time())
    host = settings.LIVE_HOST
    path = "/api/v2/product/get_item_base_info"
    code = shopee.code
    shop_id = shopee.shop_id
    access_token = shopee.access_token
    partner_id = partner_id
    partner_key = partner_key

    tmp_base_string = "%s%s%s%s%s" % (partner_id, path, timestamp, access_token, shop_id)
    base_string = tmp_base_string.encode()

    sign = hmac.new(bytes(partner_key, 'latin-1'), base_string, hashlib.sha256).hexdigest()

    product_list = ','.join(str(x) for x in product_list)

    url = host + path + "?shop_id=%s&need_tax_info=%s&item_id_list=%s&partner_id=%s&need_complaint_policy=%s&access_token=%s&timestamp=%s&sign=%s" % (
        shop_id, 'true', product_list, partner_id, False, access_token, timestamp, sign)

    resp = requests.get(url)
    return json.loads(resp.content)


def get_shopee_variant_product(shopee, partner_id, partner_key, item_id):
    timestamp = int(time.time())
    host = settings.LIVE_HOST
    path = "/api/v2/product/get_model_list"
    code = shopee.code
    shop_id = shopee.shop_id
    access_token = shopee.access_token
    partner_id = partner_id
    partner_key = partner_key

    tmp_base_string = "%s%s%s%s%s" % (partner_id, path, timestamp, access_token, shop_id)
    base_string = tmp_base_string.encode()

    sign = hmac.new(bytes(partner_key, 'latin-1'), base_string, hashlib.sha256).hexdigest()

    url = host + path + "?shop_id=%s&item_id=%s&partner_id=%s&access_token=%s&timestamp=%s&sign=%s" % (
        shop_id, item_id, partner_id, access_token, timestamp, sign)

    resp = requests.get(url)
    return json.loads(resp.content)


class ProductListView(LoginRequiredMixin, TemplateView):
    template_name = 'products/product_list.html'


class ProductDatatablesJsonView(BaseDatatableView):
    columns = ['id', 'product', 'variant', 'color', 'SKU', 'origin_price', 'stock', 'updated_at']

    def get_initial_queryset(self):
        return ProductsVariantsColors.objects.all().order_by('product')

    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        qs = qs.filter(is_deleted=False)
        if search:
            qs = qs.filter(product__name__icontains=search)

        return qs

    def prepare_results(self, qs):
        product_variant_list = []
        for product_variant_item in qs:
            product_variant_list.append({
                'id': product_variant_item.pk,
                'product': product_variant_item.product.name,
                'variant': product_variant_item.variant.name.title() if product_variant_item.variant else '-',
                'color': product_variant_item.color.name.title() if product_variant_item.color else '-',
                'SKU': '-',
                'origin_price': product_variant_item.origin_price,
                'stock': product_variant_item.stock,
                'updated_at': product_variant_item.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            })
        return product_variant_list


class SynchronizeProduct(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        if self.request.is_ajax():
            shopee = Marketplaces.objects.filter(name='SHOPEE_LIVE').first()

            shop_id = shopee.shop_id
            access_token = shopee.access_token
            refresh_token = shopee.refresh_token
            partner_id = settings.LIVE_PARTNER_ID
            partner_key = settings.LIVE_KEY

            has_next_page = True
            offset = 0
            product_list = []

            while has_next_page:
                product_list_response = get_shopee_product_list(shopee, partner_id, partner_key, offset)

                if product_list_response['error'] == 'error_auth' and \
                        product_list_response['message'] == 'Invalid access_token.':
                    access_token = refresh_shopee_access_token(shop_id, partner_id, partner_key, refresh_token)
                    product_list_response = get_shopee_product_list(shopee, partner_id, partner_key, offset)

                has_next_page = product_list_response['response']['has_next_page']
                offset = product_list_response['response']['next_offset'] if has_next_page else 0
                items = product_list_response['response']['item']
                for item in items:
                    product_list.append(item['item_id'])
                print(len(product_list))

            detail_product_list = []
            divided_list_by_50 = [product_list[i:i + 50] for i in range(0, len(product_list), 50)]
            for list in divided_list_by_50:
                detail_product_response = get_shopee_product_list_base_info(shopee, partner_id, partner_key, list)
                detail_products = detail_product_response['response']['item_list']

                for detail_product in detail_products:
                    detail_product_list.append(detail_product)

            try:
                with transaction.atomic():
                    for product_item in detail_product_list:
                        product = Products.objects.update_or_create(
                            shopee_id=product_item['item_id'],
                            defaults={
                                'name': product_item['item_name'],
                                'shopee_status': product_item['item_status']
                            }
                        )
                        variant_product_response = get_shopee_variant_product(shopee, partner_id, partner_key,
                                                                              product_item['item_id'])
                        variant_product = variant_product_response['response']

                        color_list = []
                        motif_list = []
                        for variant in variant_product['tier_variation']:
                            if 'warna' in variant['name'].lower():
                                for color_variant in variant['option_list']:
                                    product_color = Colors.objects.get_or_create(name=color_variant['option'].lower())
                                    color_list.append(product_color)
                            elif 'motif' in variant['name'].lower():
                                for motif_variant in variant['option_list']:
                                    product_motif = Variants.objects.get_or_create(name=motif_variant['option'].lower())
                                    motif_list.append(product_motif)

                        for model in variant_product['model']:
                            ProductsVariantsColors.objects.update_or_create(
                                shopee_id=model['model_id'],
                                defaults={
                                    'origin_price': model['price_info'][0]['original_price'],
                                    'stock': model['stock_info_v2']['summary_info']['total_available_stock'],
                                    'color': color_list[model['tier_index'][0]][0] if len(color_list) else None,
                                    'variant': motif_list[model['tier_index'][1]][0] if len(motif_list) else None,
                                    'product': product[0]
                                }
                            )
                    return JsonResponse({
                        'message': 'Sync data success',
                    }, status=200)
            except DatabaseError as e:
                print("Database Error: ")
                return JsonResponse({
                    'message': str(e),
                }, status=400)
