from django.db import models

# Create your models here.

class UserIndex(models.Model):
    id = models.AutoField(primary_key=True)
    unique_name = models.CharField(max_length=150, unique=True)
    username = models.CharField(max_length=150)
    email = models.EmailField(max_length=254, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(UserIndex, on_delete=models.CASCADE)
    stock_id = models.CharField(max_length=50)
    company_name = models.CharField(max_length=100)
    buy_quantity = models.PositiveIntegerField()
    buy_price = models.DecimalField(max_digits = 100, decimal_places=6)
    buy_date = models.DateField()
    current_price = models.DecimalField(max_digits = 100, decimal_places=6)
    total_investment = models.DecimalField(max_digits = 100, decimal_places=4)
    sold_quantity = models.PositiveIntegerField(default=0)
    sold_price = models.DecimalField(max_digits = 100, decimal_places=6, default=0.0)
    sold_date = models.DateField(null=True, blank=True)
    todays_profit_loss = models.DecimalField(max_digits = 100, decimal_places=6, default=0.0)
    profit_loss = models.DecimalField(max_digits = 100, decimal_places=6, default=0.0)

    
    def __str__(self):
        return f"{self.user.username} - {self.stock_id}"
