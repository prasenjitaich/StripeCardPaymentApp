from django.urls import path
from .views import *

urlpatterns = [
    path('create-payment-intent/', CreatePayment.as_view(), name='create_payment'),
    path('refund-payment-intent/', CreateRefund.as_view(), name='create_refund'),
    path('cancel-payment-intent/', CancelPaymentIntent.as_view(), name='cancel_intent'),
    path('card-manage/', CardManagement.as_view(), name='card_management'),
    path('default-card/', DefaultCard.as_view(), name='default_card'),
    path('webhook/', WebhookView.as_view(), name='webhook_view'),
]
