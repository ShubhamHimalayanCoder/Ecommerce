from django.db import models
from Seller import models as seller_models

# Create your models here.

class Customer_data(models.Model):
    customer_id=models.AutoField(primary_key=True, unique=True)
    customer_name=models.CharField(max_length=100)
    customer_email=models.EmailField(max_length=100)
    customer_password=models.CharField(max_length=20)
    customer_gender=models.CharField(max_length=10)
    customer_role=models.CharField(max_length=20)
    customer_phone=models.CharField(max_length=10)
    customer_address = models.TextField(null=True)

    def __str__(self) -> str:
        return f"Customer_ID : {self.customer_id}, Customer_Name : {self.customer_name}"
    


class Cart(models.Model):
    customer=models.ForeignKey(Customer_data,related_name='customer', on_delete=models.CASCADE)
    product=models.ForeignKey(seller_models.Product_data,related_name='product', on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return f"Product : {self.product.product_name}, Quantity : {self.quantity}"
    

class Order(models.Model):
    customer=models.ForeignKey(Customer_data, on_delete=models.CASCADE)
    product=models.ForeignKey(seller_models.Product_data, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    order_date=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Order_by: {self.customer.customer_name}, Product : {self.product.product_name}"
