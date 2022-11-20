from django.urls import path, include
from .views import (
    banklists,
    paymentmethodlists,
    addBank,
    singleBank,
    updateBank,
    deleteBank,
    addPaymentMethod,
    singlePaymentMethod,
    updatePaymentMethod,
    deletePaymentMethod,
)

urlpatterns = [
    path("banks/", banklists),
    path("payment-methods/", paymentmethodlists),
    path("add-bank/", addBank),
    path("bank-single/<int:id>/", singleBank),
    path("update-bank/", updateBank),
    path("delete-bank/", deleteBank),
    path("add-payment-method/", addPaymentMethod),
    path("payment-method-single/<int:id>/", singlePaymentMethod),
    path("update-payment-method/", updatePaymentMethod),
    path("delete-payment-method/", deletePaymentMethod),
]
