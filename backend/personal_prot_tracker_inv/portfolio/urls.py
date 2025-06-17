from django.urls import path
from . import views

urlpatterns = [
    # URL for listing all available assets (e.g., stocks, crypto)
    # GET /api/portfolio/assets/
    path('assets/', views.AssetList.as_view(), name='asset-list'),
    
    # URL for viewing the current user's portfolio details
    # GET /api/portfolio/
    path('', views.PortfolioDetail.as_view(), name='portfolio-detail'),
    
    # URL for listing and creating transactions for the current user
    # GET, POST /api/portfolio/transactions/
    path('transactions/', views.TransactionListCreate.as_view(), name='transaction-list-create'),
]