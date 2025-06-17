from rest_framework import serializers
from .models import Asset, Portfolio, Transaction, PortfolioAsset, Watchlist
from django.contrib.auth.models import User
import yfinance as yf # Import yfinance



# ---  HELPER FUNCTION ---
def get_or_create_asset_from_ticker(ticker_symbol):
    """
    Checks if a ticker is valid using yfinance.
    If valid and not in DB, creates it.
    Returns the Asset object or None if invalid.
    """
    ticker_symbol = ticker_symbol.upper()
    try:
        # Check if the asset already exists in our DB
        asset = Asset.objects.get(ticker=ticker_symbol)
        return asset
    except Asset.DoesNotExist:
        # If not, query yfinance to see if it's a real ticker
        stock = yf.Ticker(ticker_symbol)
        # .info is a quick way to check for validity. If it's invalid,
        # it will often be empty or missing a key like 'shortName'.
        if not stock.info or 'shortName' not in stock.info:
            return None # Ticker is not valid
        
        # If valid, create it in our database
        asset = Asset.objects.create(ticker=ticker_symbol)
        return asset


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'ticker']

# A serializer for our summary model, PortfolioAsset.
# This is what we'll use to show the user's current holdings.
class PortfolioAssetSerializer(serializers.ModelSerializer):
    # We want to show the full asset details, not just its ID.
    asset = AssetSerializer(read_only=True)
    
    class Meta:
        model = PortfolioAsset
        fields = ['id', 'asset', 'quantity', 'average_cost']

# The main serializer for the Portfolio, which includes all its assets.
class PortfolioSerializer(serializers.ModelSerializer):
    # Use the PortfolioAssetSerializer for the nested 'assets' relationship.
    # 'many=True' because a portfolio can have many assets.
    assets = PortfolioAssetSerializer(many=True, read_only=True)
    
    class Meta:
        model = Portfolio
        fields = ['id', 'user', 'name', 'assets']

# Serializer for creating and listing transactions.
class TransactionSerializer(serializers.ModelSerializer):
    # Display the user's username instead of their ID.
    # read_only=True because we will set the user automatically in the view.
    user = serializers.StringRelatedField(read_only=True)

    # We now accept a ticker string from the frontend, not an asset ID.
    ticker = serializers.CharField(write_only=True, max_length=10)

    # We want to be able to create a transaction by sending the asset's ID.
    # 'queryset' is needed for validation by DRF.
    asset = AssetSerializer(read_only=True)

    class Meta:
        model = Transaction
        # We don't need to expose 'user' for creation, it's set automatically.
        fields = ['id', 'user', 'asset', 'ticker', 'transaction_type', 'quantity', 'price', 'transaction_date']
       
        # Custom validation for the 'ticker' field.
    def validate_ticker(self, value):
        asset = get_or_create_asset_from_ticker(value)
        if asset is None:
            raise serializers.ValidationError(f"Invalid or unsupported ticker: {value}")
        return asset # Return the asset object, not the string

    def create(self, validated_data):
        """
        Override create to handle the 'ticker' field correctly.
        """
        # The 'ticker' field was validated and turned into an 'asset' object.
        # We rename it before creating the transaction.
        validated_data['asset'] = validated_data.pop('ticker')
        return Transaction.objects.create(**validated_data)


class WatchlistSerializer(serializers.ModelSerializer):
    # Same as transaction serializer, we accept a ticker string for creation
    ticker = serializers.CharField(write_only=True, max_length=10)
    asset = AssetSerializer(read_only=True)

    class Meta:
        model = Watchlist
        fields = ['id', 'asset', 'ticker']

    def validate_ticker(self, value):
        asset = get_or_create_asset_from_ticker(value)
        if asset is None:
            raise serializers.ValidationError(f"Invalid or unsupported ticker: {value}")
        return asset

    def create(self, validated_data):
        # Get the current user from the view's context
        user = self.context['request'].user
        asset = validated_data.pop('ticker')
        
        # Use get_or_create to prevent adding duplicates, which would violate the constraint
        watchlist_item, created = Watchlist.objects.get_or_create(user=user, asset=asset)
        return watchlist_item