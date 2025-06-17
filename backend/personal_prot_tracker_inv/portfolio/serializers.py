from rest_framework import serializers
from .models import Asset, Portfolio, Transaction, PortfolioAsset
from django.contrib.auth.models import User

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'ticker', 'name']

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

    # We want to be able to create a transaction by sending the asset's ID.
    # 'queryset' is needed for validation by DRF.
    asset = serializers.PrimaryKeyRelatedField(queryset=Asset.objects.all())

    class Meta:
        model = Transaction
        # We don't need to expose 'user' for creation, it's set automatically.
        fields = ['id', 'user', 'asset', 'transaction_type', 'quantity', 'price', 'transaction_date']
        # Make some fields read-only in the API context
        read_only_fields = ['user', 'transaction_date']