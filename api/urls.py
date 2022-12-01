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
    vatlists,
    taxlists,
    vatandtaxlists,
    addTax,
    updateTax,
    deleteTax,
    singleTax,
    addVat,
    updateVat,
    deleteVat,
    singleVat,
    completeorder,
    cancleapyment,
    cancleorder,
    paymentorderlists,
    paymentlists_report,
    paymentorderlistsingle,
    orderslists_report,
    kot_printed,
    all_report,
    CustomAuthToken,
)

urlpatterns = [
    path("order-report/", orderslists_report),
    path("all-report/", all_report),
    path("payment-report/", paymentlists_report),
    path("foodlists/", foodlists),
    path("foodlists_search/", foodlists_search),
    path("categorylists/", categorylists),
    path("orderslists/", orderslists),
    path("paymentorderlists/", paymentorderlists),
    path("submitcart/", submitcart),
    path("cancel-payment/<int:id>/", cancleapyment),
    path("complete-order/<int:id>/", completeorder),
    path("print-kot/<int:id>/", kot_printed),
    path("cancel-order/<int:id>/", cancleorder),
    path("payment-single/<int:id>/", paymentorderlistsingle),
    path("payorders/", paymentt),
    path("tablelists/", tablelists),
    path("add-table/", addTable),
    path("table-single/<int:id>/", singleTable),
    path("update-table/", updateTable),
    path("delete-table/", deleteTable),
    path("vat-and-tax/", vatandtaxlists),
    path("vats/", vatlists),
    path("taxes/", taxlists),
    path("add-vat/", addVat),
    path("vat-single/<int:id>/", singleVat),
    path("update-vat/", updateVat),
    path("delete-vat/", deleteVat),
    path("add-tax/", addTax),
    path("tax-single/<int:id>/", singleTax),
    path("update-tax/", updateTax),
    path("delete-tax/", deleteTax),
    path("inventory/", include("inventory.urls")),
    path("payment/", include("payments.urls")),
    path("account/", include("accounts.urls")),
    path("api-token-auth/", CustomAuthToken.as_view(), name="api_token_auth"),
]
