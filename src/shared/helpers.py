import hmac
import json
import time
import requests
import hashlib

from django.conf import settings
from django.db import DatabaseError

from src.marketplace.models import Marketplaces
from src.shared.enum import MarketplaceName


def refresh_shopee_access_token(shop_id, partner_id, partner_key, refresh_token):
    timestamp = int(time.time())
    host = settings.LIVE_HOST
    path = "/api/v2/auth/access_token/get"
    body = {"shop_id": int(shop_id), "refresh_token": refresh_token, "partner_id": int(partner_id)}
    tmp_base_string = "%s%s%s" % (partner_id, path, timestamp)
    base_string = tmp_base_string.encode()
    partner_key = partner_key.encode()
    sign = hmac.new(partner_key, base_string, hashlib.sha256).hexdigest()
    url = host + path + "?partner_id=%s&timestamp=%s&sign=%s" % (partner_id, timestamp, sign)
    headers = {"Content-Type": "application/json"}

    try:
        resp = requests.post(url, json=body, headers=headers)
    except:
        print('error')
        return

    ret = json.loads(resp.content)
    access_token = ret.get("access_token")
    new_refresh_token = ret.get("refresh_token")

    if access_token is not None or new_refresh_token is not None:
        try:
            M = Marketplaces.objects.filter(name='SHOPEE_LIVE').update(access_token=access_token, refresh_token=new_refresh_token)
        except DatabaseError:
            print('error')

    return access_token, new_refresh_token


