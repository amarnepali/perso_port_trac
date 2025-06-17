from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Asset, Portfolio, Transaction, Watchlist
from .serializers import (
    AssetSerializer,
    PortfolioSerializer,
    TransactionSerializer,
    WatchlistSerializer

)

# --- Asset Views ---
# Anyone can view the list of available assets.
class AssetList(generics.ListAPIView):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    # No authentication needed for this, but you could change it
    permission_classes = [permissions.AllowAny]


# --- Portfolio Views ---
# Only the owner of the portfolio can view it.
class PortfolioDetail(generics.RetrieveAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Overrides the default get_object to return the portfolio
        for the currently authenticated user.
        """
        # We can create the portfolio if it doesn't exist for the user yet.
        # This is a handy way to auto-provision resources for new users.
        portfolio, created = Portfolio.objects.get_or_create(user=self.request.user)
        return portfolio


# --- Transaction Views ---
# A user can list their own transactions or create a new one.
class TransactionListCreate(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should only return transactions for the currently
        authenticated user.
        """
        return Transaction.objects.filter(user=self.request.user).order_by('-transaction_date')

    def perform_create(self, serializer):
        """
        This method is called by DRF when creating a new object.
        We override it to automatically set the user to the one making the request.
        """
        # First, ensure the asset exists. The serializer validates this.
        asset = serializer.validated_data.get('asset')
        
        # Now, save the transaction with the current user.
        serializer.save(user=self.request.user)
        
       

class WatchlistListCreateView(generics.ListCreateAPIView):
    serializer_class = WatchlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return watchlist items for the current user."""
        return Watchlist.objects.filter(user=self.request.user)

class WatchlistItemDestroyView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Ensure users can only delete their own watchlist items."""
        return Watchlist.objects.filter(user=self.request.user)
