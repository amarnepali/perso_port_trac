from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint

# Represents a stock, crypto, etc.
# The Asset model is now simpler. It's just a verified ticker.
# yfinance will give us the name and other data.
class Asset(models.Model):
    ticker = models.CharField(max_length=20, unique=True)
    # name = models.CharField(max_length=100)
    # # You could add asset type (stock, crypto, etc.) here
    # asset_type = models.CharField(max_length=10, default='STOCK')

    def __str__(self):
        return self.ticker

# The user's main portfolio
class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='My Portfolio')

    def __str__(self):
        return f"{self.user.username}'s Portfolio"

# A single buy or sell action
class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    )
    # Link to the user who made the transaction
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    quantity = models.DecimalField(max_digits=18, decimal_places=8)
    price = models.DecimalField(max_digits=18, decimal_places=8) # Price per unit
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} {self.quantity} of {self.asset.ticker} by {self.user.username}"

# A summary table for efficient lookups. This is the "smart" part.
# It stores the current calculated state of a user's holding in a single asset.
class PortfolioAsset(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='assets')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=18, decimal_places=8)
    average_cost = models.DecimalField(max_digits=18, decimal_places=8)

    class Meta:
        # Ensures a user can't have two entries for the same asset in their portfolio
        constraints = [
            UniqueConstraint(fields=['portfolio', 'asset'], name='unique_portfolio_asset')
        ]

    def __str__(self):
        return f"{self.quantity} of {self.asset.ticker} in {self.portfolio.name}"
    


# NEW MODEL: The user's watchlist
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)

    class Meta:
        # A user can only have a specific asset on their watchlist once.
        constraints = [
            models.UniqueConstraint(fields=['user', 'asset'], name='unique_user_asset_watchlist')
        ]

    def __str__(self):
        return f"{self.user.username}'s watchlist: {self.asset.ticker}"