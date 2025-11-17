from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AdViewSet, 
    ExchangeProposalViewSet,
    AdListView,
    AdDetailView,
    AdCreateView,
    AdUpdateView,
    AdDeleteView,
    ExchangeProposalCreateView,
    ExchangeProposalListView,
    accept_exchange_proposal,
    reject_exchange_proposal,
    AdSearchView
)

router = DefaultRouter()
router.register(r'ads', AdViewSet, basename='api-ad')
router.register(r'proposals', ExchangeProposalViewSet, basename='api-proposal')

app_name = 'ads'

api_urlpatterns = [
    path('', include(router.urls)),
]

html_urlpatterns = [
    path('', AdListView.as_view(), name='list'),
    path('create/', AdCreateView.as_view(), name='create'),
    path('<int:pk>/', AdDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', AdUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', AdDeleteView.as_view(), name='delete'),
    path('<int:ad_id>/propose/', ExchangeProposalCreateView.as_view(), name='propose_exchange'),
    path('exchange-proposals/', ExchangeProposalListView.as_view(), name='exchange_proposals'),
    path('exchange-proposals/<int:pk>/accept/', accept_exchange_proposal, name='accept_proposal'),
    path('exchange-proposals/<int:pk>/reject/', reject_exchange_proposal, name='reject_proposal'),
    path('search/', AdSearchView.as_view(), name='search')
]

urlpatterns = [
    path('api/', include((api_urlpatterns, 'api'))),
    path('', include(html_urlpatterns)),
]


# from django.urls import path, include


# from rest_framework.routers import DefaultRouter
# from .views import (
#     AdViewSet, 
#     ExchangeProposalViewSet,
#     AdListView,
#     AdDetailView,
#     AdCreateView,
#     AdUpdateView,
#     AdDeleteView,
#     ExchangeProposalCreateView,
#     ExchangeProposalListView,
#     accept_exchange_proposal,
#     reject_exchange_proposal,
#     ExchangeProposalCreateAPIView,
#     AdDeleteAPIView
# )

# router = DefaultRouter()
# router.register(r'ads', AdViewSet, basename='ad')
# router.register(r'proposals', ExchangeProposalViewSet, basename='proposal')
# app_name = 'ads'



# urlpatterns = [
#     # API URLs
#     path('api/', include(router.urls)),
#     path('', AdListView.as_view(), name='list'),
#     path('<int:pk>/create/', AdUpdateView.as_view(), name='update'),
#     path('<int:pk>/', AdDetailView.as_view(), name='detail'),
#     path('create/', AdCreateView.as_view(), name='create'),
#     path('<int:pk>/delete/', AdDeleteView.as_view(), name='delete'),
#     path('<int:ad_id>/propose/', ExchangeProposalCreateView.as_view(), name='propose_exchange'),
#     path('exchange-proposals/', ExchangeProposalListView.as_view(), name='exchange_proposals'),
#     path('exchange-proposals/<int:pk>/accept/', accept_exchange_proposal, name='accept_proposal'),
#     path('exchange-proposals/<int:pk>/reject/', reject_exchange_proposal, name='reject_proposal'),
    
#     path('api/<int:pk>/update/', ExchangeProposalCreateAPIView.as_view(), name='api-proposal-update'),
#     path('api/<int:pk>/delete/', AdDeleteAPIView.as_view(), name='api-ad-delete')
# ]