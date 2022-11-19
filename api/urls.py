from django.urls import path, include
from .views import (
    foodlists,
    submitcart,
    orderslists,
    categorylists,
    foodlists_search,
    paymentt,
    tablelists,
    addTable,
    updateTable,
    deleteTable,
    singleTable,
    CustomAuthToken,
)

urlpatterns = [
    path("foodlists/", foodlists),
    path("foodlists_search/", foodlists_search),
    path("categorylists/", categorylists),
    path("orderslists/", orderslists),
    path("submitcart/", submitcart),
    path("payorders/", paymentt),
    path("tablelists/", tablelists),
    path("add-table/", addTable),
    path("table-single/<int:id>/", singleTable),
    path("update-table/", updateTable),
    path("delete-table/", deleteTable),
    path("inventory/", include("inventory.urls")),
    path("api-token-auth/", CustomAuthToken.as_view(), name="api_token_auth"),
]
