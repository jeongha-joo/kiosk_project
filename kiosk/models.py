from django.db import models


# Create your models here.
class content(models.Model):
    goods_name = models.CharField(max_length=50)
    goods_price = models.IntegerField()
    def __str__(self):
        return self.goods_name

class order_time(models.Model):
    order_time = models.DateTimeField()
    def __str__(self):
        return f"주문 시간: {self.order_time}"

class order_bill(models.Model):
    order_id = models.ForeignKey(order_time, on_delete=models.SET_NULL,null=True)
    goods_id = models.ForeignKey(content, on_delete=models.CASCADE)
    goods_count = models.IntegerField()
    def __str__(self):
        return f"{self.order_id}"

class customer_bill(models.Model):
    order_id = models.ForeignKey(order_time, on_delete=models.SET_NULL,null=True)
    payment = models.IntegerField()
    payment_method = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.order_id}"


