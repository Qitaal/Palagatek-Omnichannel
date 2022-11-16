import hashlib
import json
import hmac
import requests
import time

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, RedirectView

from src.marketplace.models import Marketplaces
from src.shared.enum import MarketplaceName


class MarketplaceListView(LoginRequiredMixin, TemplateView):
    template_name = 'marketplaces/list.html'


class ShopeeGenerateAuthLink(LoginRequiredMixin, RedirectView):

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        timestamp = int(time.time())
        host = settings.TEST_HOST
        path = "/api/v2/shop/auth_partner"
        redirect_url = "http://127.0.0.1:8000/marketplace/get_shopee_access_token"
        partner_id = settings.TEST_PARTNER_ID
        key = settings.TEST_KEY
        partner_key = key.encode()
        tmp_base_string = "%s%s%s" % (partner_id, path, timestamp)
        base_string = tmp_base_string.encode()
        sign = hmac.new(partner_key, base_string, hashlib.sha256).hexdigest()
        url = host + path + "?partner_id=%s&timestamp=%s&sign=%s&redirect=%s" % (
        partner_id, timestamp, sign, redirect_url)

        return url


class AuthShopee(LoginRequiredMixin, RedirectView):

    def get(self, request, *args, **kwargs):
        code = request.GET.get('code', None)
        shop_id = request.GET.get('shop_id', None)
        partner_id = settings.TEST_PARTNER_ID

        if code and shop_id:
            timestamp = int(time.time())
            host = settings.TEST_HOST
            path = "/api/v2/auth/token/get"
            body = {"code": code, "shop_id": int(shop_id), "partner_id": int(partner_id)}
            tmp_base_string = "%s%s%s" % (partner_id, path, timestamp)
            base_string = tmp_base_string.encode()
            partner_key = settings.TEST_KEY
            sign = hmac.new(bytes(partner_key, 'latin-1'), base_string, hashlib.sha256).hexdigest()
            url = host + path + "?partner_id=%s&timestamp=%s&sign=%s" % (partner_id, timestamp, sign)
            headers = {"Content-Type": "application/json"}
            resp = requests.post(url, json=body, headers=headers)
            ret = json.loads(resp.content)
            access_token = ret.get("access_token")
            new_refresh_token = ret.get("refresh_token")
            Marketplaces.objects.update_or_create(
                name=MarketplaceName.SHOPEE,
                defaults={
                    'access_token': access_token,
                    'refresh_token': new_refresh_token,
                    'code': code,
                    'shop_id': shop_id
                })
        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('marketplace:marketplace_list')

