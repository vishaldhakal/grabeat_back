# API Endpoints

1. https://grabeatnp.herokuapp.com/api/api-token-auth/
   Input : Username and Password
   Output : Token, Username and Usertype

###

3. https://grabeatnp.herokuapp.com/api/categorylists/
   Output : List of all food categories

###

4. https://grabeatnp.herokuapp.com/api/foodlists/
   Output : List of all fooditems

###

5. https://grabeatnp.herokuapp.com/api/foodlists_search/
   Input : category and sorting [By price ascending or descending]
   Output : List of all fooditems

### Table Management

2. https://grabeatnp.herokuapp.com/api/tablelists/
   Output : List of all tables

###

3. https://grabeatnp.herokuapp.com/api/add-table/
   Input : Table Name
   Output : Success or error message

###

7. https://grabeatnp.herokuapp.com/api/update-table/
   Input : Table Id
   Output : Success or error message

###

8. https://grabeatnp.herokuapp.com/api/table-single/<int:id>/
   Input : Table Id
   Output : Table with that id

###

9. https://grabeatnp.herokuapp.com/api/delete-table/
   Input : Table Id
   Output : Success or error message

path("/api/vat-and-tax/", vatandtaxlists),
path("/api/vats/", vatlists),
path("/api/taxes/", taxlists),
path("/api/add-vat/", addVat),
path("/api/vat-single/<int:id>/", singleVat),
path("/api/update-vat/", updateVat),
path("/api/delete-vat/", deleteVat),
path("/api/add-tax/", addTax),
path("/api/tax-single/<int:id>/", singleTax),
path("/api/update-tax/", updateTax),
path("/api/delete-tax/", deleteTax),

path("/api/payment/banks/", banklists),
path("/api/payment/payment-methods/", paymentmethodlists),
path("/api/payment/add-bank/", addBank),
path("/api/payment/bank-single/<int:id>/", singleBank),
path("/api/payment/update-bank/", updateBank),
path("/api/payment/delete-bank/", deleteBank),
path("/api/payment/add-payment-method/", addPaymentMethod),
path("/api/payment/payment-method-single/<int:id>/", singlePaymentMethod),
path("/api/payment/update-payment-method/", updatePaymentMethod),
path("/api/payment/delete-payment-method/", deletePaymentMethod),
