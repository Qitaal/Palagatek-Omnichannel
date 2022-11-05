from django.db import models


class Provinces(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'provinces'

    def __str__(self):
        return self.name


class Cities(models.Model):
    name = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=5)
    province_id = models.ForeignKey(Provinces, on_delete=models.CASCADE)

    class Meta:
        db_table = 'cities'

    def __str__(self):
        return self.name


class Subdistricts(models.Model):
    name = models.CharField(max_length=255)
    city_id = models.ForeignKey(Cities, on_delete=models.CASCADE)

    class Meta:
        db_table = 'subdistricts'

    def __str__(self):
        return self.name
