# API Endpoints

1. https://grabeatnp.herokuapp.com/api/api-token-auth/
   Input : Username and Password
   Output : Token, Username and Usertype

###

2. https://grabeatnp.herokuapp.com/api/tablelists/
   Output : List of all tables

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

6. https://grabeatnp.herokuapp.com/api/add-table/
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
