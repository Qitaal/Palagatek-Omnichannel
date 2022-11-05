from django.db import models


class OrderStatus (models.TextChoices):
    UNPAID = 'UNPAID'
    NEED_TO_PROCESS = 'NEED_TO_PROCESS'
    CANCELED = 'CANCELED'
    PROCESSED = 'PROCEED'
    ON_DELIVERY = 'ON_DELIVERY'
    COMPLETED = 'COMPLETED'


class ShopeeStatus (models.TextChoices):
    NORMAL = 'NORMAL'
    BANNED = 'BANNED'
    DELETED = 'DELETED'
    UNLIST = 'UNLIST'
