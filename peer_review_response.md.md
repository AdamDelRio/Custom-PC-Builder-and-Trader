# Peer Review Response

## Code Review Comments


### Suhanth Alluri

1. Verify that there is enough of an item in inventory when checking out, provide error message if there is not enough
- **Good idea. That can prevent commiting changes or transactions. Fixing this week.**

- **FIX: if statement after select statement**

2. Add some kind of concurrency control as there can be multiple checkouts at the same time.
- **Potentially adding this control - not sure if adding isolation level would work**
- **FIX: Not sure which isolation level to do yet, or what to do - locking/not locking, etc.**

3. Add logging for different interactions, error messages, can make it easier to keep track of things or figure out what caused issues

- **FIX: Add logger and print statements in more spots with variables being returned**

4. Validate that an email is a valid email address
- **FIX: plan to import email from python to validate email inputs**


5. Consider letting user login with username or email
- **IGNORED: Using OAUTH**
6. When logging in, specify whether it's the email or username that was already taken for better UX.
- **IGNORED: Using OAUTH**
7. Consider adding docstrings describing the purpose of some functions for the functions that don't already have this.
- **IGNORED: Good idea, but not necessary at the moment for how much time we have**
8. For the search, consider using ILIKE for case-insensitive search, and maybe functionality to filter search
- **FIX: Add ILIKE to search query**
9. When there are no search results, add a message indicating this is the case
- **FIX: adding return statements within conditional if no results**
10. Add comment/docstring specifying the difference between get_user_catalog() and get_user_catalog_for_user().
- **Fixing with idea 7 above**
11. Add data validation and provide appropriate error messages for invalid data.
- **FIX: Check inputs**
12. Write get_catalog() query as multiline docstrings for readability.
- **FIX: with idea 7**

### Mio Nakagawa

1. Maybe add a password for the login

**Fix:** Using OAuth

2. Maybe add a ledger system for keeping track of the parts

**Fix:** Our current schema doesn't support ledgers and we do not feel as though it is needed

3. Deleting cart items during checkout might lead to a loss in track of history

**Fix:** Created 'CheckedOut' column in table

4. Maybe add a transaction history table to ledgerize

**Fix:** This is already done

5. Maybe have a way to differentiate users when they are selling vs buying

**Fix:** We beleive that all users should be able to both buy and sell, so we don't believe this is necessary 

6. Maybe subtract the price of the parts when checking out

**Fix:** We currently don't support users having a balance, so there is nothing to subtract from

7. When checking out, check to see if there is enough inventory of that specific item they are checking out

**Fix:** 

Added this check in `set_item_quantity` to make sure the item exists and enough quantity exists in the catalog 

```
inventory_table = "user_parts" if cart_item.user_item else "part_inventory"
inventory_id_column = "id" if cart_item.user_item else "part_id"

inventory_item = connection.execute(
    sqlalchemy.text(
        f"SELECT quantity FROM {inventory_table} WHERE {inventory_id_column} = :part_id"
    ).params(part_id=part_id)
).fetchone()

if inventory_item and inventory_item.quantity >= cart_item.quantity:
```

8. For the sql query such as sqlalchemy.text("SELECT id FROM customers WHERE “ “name = :name AND address = :address AND “ “phone = :phone AND email = :email”), you could change it so that you add a backslash, then you would not have to include double quotations: sqlalchemy.text("SELECT id FROM customers WHERE \ name = :name AND address = :address AND \ phone = :phone AND email = :email")

**Fix:** Don't feel as though this is necessary

9. Since you are returning the temp_id for create_template, maybe also return the id for add_item_to_template in templates.py

**Fix:** Will do this

10. Maybe have an error handling in place in case when checkout is unable to be done

**Fix:** Will do this

11. What happens if multiple people try to checkout the same thing at the same time

**Fix:** Going to add this error handeling

12. When updating items in the catalog, maybe make it so that you ledgerize and sum up the quantity

**Fix:** Again, don't feel as though ledgers fit in our schema

### Hallie Christopherson

1. In templates.py, move the return statement in the add_item_to_template function to be within the “with” instead of outside

**Fix:** We moved the return inside the connection.

2. Reformat SQL queries so that they are more readable (from carts, create_cart)
        SELECT id
        FROM customers
        WHERE name = :name
            AND address = :address
            AND phone = :phone
            AND email = :email 
            
**Fix:** Did not reformat, looking over the SQL query that the reviewer mentioned we felt it was already very readable and saw no reason to alter it.

3. Add more exception checking in the add_to_user_catalog function similar to the beginning of the function. For example, if the second SQL statement is using a user_id that is invalid, raise an error.

**Fix:** We added constraints on the datatable instead. For instance in the user_parts table (which is what the add_to_user_catalog inserts into) we added constraint: user_parts_quantity_check check ((quantity >= 0)). Additionally since the user_id is a foreign key already it will not allow users to add a user_id that does not exist.

4. Rather than returning “ok” in the set_item_quantity function in carts, try returning more helpful information, such as the cart_id or the cart_item. In addition, move this return statement to be inside the “with”.

**Fix:** Did not feel any additional information was needed for setting item quantity in a datatable other than success. However did move the return inside the "with".

5. In your checkout function in carts.py, I would not include the delete statement as this is erasing information that could be helpful in debugging and tracking order history. Long term this may not be something you must keep track of however I would keep all history in cart_items for now.

**Fix:** Added a checked_out boolean column for cart_items table and instead of deleting from cart_items now just update this column.

6. Move the return statement in carts.py so that it is within the with statement of the checkout function in carts.py.

**Fix:** Moved the return statement

7. Reformat the SQL statement in catalog/get_catalog so that it is more readable and not one long string.

**Fix:** Did not fix, the SQL statement in `get_catalog` is already very readable and does not need to be altered.

8. The for loop in get_catalog should be within the “with” statement to avoid concurrency issues.

**Fix:** Moved the return inside the "with" statement.

9. I would modify your search function in a few different ways. First, I would make it so that each parameter is optional and a list of results is returned. This way, if a user only knows what type of part they want, they will still receive results and information from their search.

**Fix:** We did a complete overhaul of our search endpoint, including these suggestions. Now is a much more complex and useful endpoint.

10. Modify the add_users_to_catalog function so there are not multiple “with db.engine.begin() as connection:” statements. Everything should be within one “with” statement.

**Fix:** Removed the multiple “with db.engine.begin() as connection:” statements so it is all within a single connection.

11. Add a check in the checkout function that ensures that all items are available before checking out. If an item is not available determine how that is handled. This could be an error message that rolls back the entire transaction, or the remaining items may still be bought.

**Fix:** 

Added this check in `set_item_quantity` to make sure the item exists and enough quantity exists in the catalog 

```
inventory_table = "user_parts" if cart_item.user_item else "part_inventory"
inventory_id_column = "id" if cart_item.user_item else "part_id"

inventory_item = connection.execute(
    sqlalchemy.text(
        f"SELECT quantity FROM {inventory_table} WHERE {inventory_id_column} = :part_id"
    ).params(part_id=part_id)
).fetchone()

if inventory_item and inventory_item.quantity >= cart_item.quantity:
```

12. I recommend modifying the return statement in add_to_users catalog so that there is some error handling. Currently the function only returns “success”, and it would be more helpful to add exception handling to see if something fails.

**Fix:** Added a try/except block to catch and return error messages in `add_to_user_catalog`.

### Jinrong Pettit

1. In login.py, for sign_up() make seperate errors and error messages for if username is already taken and if email is already

**Fix:** We will add error handling messages to login.py.

2. For creating a new template specify that template id is being returned. Right now it just returns a magic number

**Fix:** We will add that to our code.

3. Return more useful messages on POST calls instead of just returning "OK". For example add_item_to_template() could say "item ... inserted into template_id ..."

**Fix:** We will change our comments to reflect more on what the post call is doing.

4. Reformat some of the SQL statements into more readable formats instead of having one long string (get_catalog)

**Fix:** We feel as if our SQL statements are readable as is.

5. Most of the endpoints in templates.py and carts.py don’t have comments specifying a short explanation on what the endpoint does

**Fix:** This could make our code much more readable, we will add somne.

6. For add_to_user_catalog() only one “db.engine.begin() as connection” is needed but there are multiple in the endpoint

**Fix:** We will put them all under one connection, this will also help with concurrency issues.

7. The description for get_user_catalog() and get_user_catalog_for_user() is the same fix the description for get_user_catalog()

**Fix:** We will change get_user_catalog() to reflect this difference.

8. In Consider more robust error handling, for example right now if I were to search for something in search_catalog() that doesn’t exist it will return an internal server error

**Fix:** We will add some error handling to this endpoint.

9. During checkout, instead of deleting the cart_item I would just keep them in order to keep track of all the orders. An alternative could be to make a table column with a boolean to indicate whether or not the cart_item has been checked out or not

**Fix:** We are adding a checked_out boolean column.

10. In carts.py, remove the CartCheckout class and cart_checkout parameter from checkout since its not being used

**Fix:** We will remove this.

11. In carts.py, for create_cart(), to decrease the amount of carts being made, you can check to see if a customer has already made a cart and if they did you don't have to make another cart and instead just return the cart_id

**Fix:** We do not find this necessary.

12. In carts.py, for checkout I would check to make sure that there is enough of a certain spec in the inventory before allowing the customer to buy it. If there isn’t enough inventory then you probably should just return

**Fix:** We added this feature in set_item_quantity instead.

13. For catalog, add_to_user_catalog(), if a user wants to sell the same item for two different prices they won't be able to do that since it will be under the same item and the price would be whatever the price that was just inserted.

**Fix:** We do not feel as if this is a big enough issue to fix.

## Schema Review Comments

### Suhanth Alluri

1. Add a password field to users so that other people cannot easily log in to your account, make sure it is encrypted for security.

**Ignoring**: Using OAuth (not implemented at the moment - storing emails as placeholder)... No need to store passwords

2. Encrypt email field in users for increased security.

**Ignoring**: Using OAuth, so no need for encrypting email fields. OAuth will handle sign ons. Might hash and salt for privacy, however. 

3. Do not allow fields in part_inventory to be nullable so that important data is not missing from this table.

**Fixed**: Updated table to not allow null values

4. Do not allow part_id to be nullable in monitor_specs, cpu_specs, case_specs table, psu_specs, video_card_specs this information is important for an entry.

**Ignored**: Already restricting null entries

5. Do not allow the fields in part_inventory to be nullable, this information is important for an entry, especially type and name.

**Ignored**: Same as idea 3... already fixed

6. Core clock and boost_clock in video_card_specs should probably be of type "real" since they are usually decimal values.

**Fixed**: Changed floats to numeric type

7. Would a boolean type be better for some of the values in case_specs? (e.g. external volume)

**Ignoring**: Data is already provided with real information. Bool would get rid of specific data 

8. In case specs, internal_35_bays most likely doesn't need to be a bigint type and can be a integer instead.

**Fixed**: Changed type to int4

9. Consider adding a flow to delete something from a template

**Ignoring**: Have remove items from template API. 

10. Having to enter address, phone, email, and name when creating a new cart seems slightly impractical. Consider having these as fields in the user table that are populated during signup so that they can be accessed with a user id.

**Good idea**: Plan to fix 

11. Consider adding a flow to delete something from a catalog in case they don't want to sell an item anymore.

**Good idea**: Plan to add

12. Record transactions and use ledgers to update item quantities in invetory, could be useful for getting user purchase history as well.

**Potential Add if Time Permits**

### Hallie Cristopherson

1. I recommend modifying the create account endpoint to take in the same information that is required when creating a cart. This way the data can later be accessed by the primary key of the user id when the user goes to create a cart. In addition, then you will have more data (such as age demographic) of the users who make accounts on your website, not just the people who add to their carts.

**Fix:** We removed having to enter the email when creating a cart, but left address and phone number since this is what is typically seen when checking out on websites (and not when creating an account).

2. Rather than having a running quantity of each item, you may want to ledgerize your part_inventory. This way you can add up the total each time and avoid the concurrency issues faced in the early stages of the potions shop.

**Fix:** We may change to a ledgerized design, if we have time, however it is not a top priority. We have added some parts for future ledgerization. However since we don't recieve a quantity (we basically just add a random number of each part), it is difficult to find a reason to ledgerize the database.

3. I would modify the search so that it is not case sensitive using the ilike function.

**Fix:** Added, redid the search function.

4. The search function could also have optional parameters. For example if a user knew the type of part they wanted and not the name, they would still be presented with options.

**Fix:** Added, redid the search function.

5. I would also add sorting functionality with the search by price as this is a common feature on websites that displays data in a form that is more helpful to customers. In addition I would add a filter by price option so that results will be displayed based on a person’s budget.

**Fix:** Added, redid the search function.

6. I would change the login endpoint to return a boolean rather than the primary key associated with their account.

**Fix:** We feel it is necessary to return the id for further use when logging in. Did not change.

7. It may be helpful to add a view template endpoint as currently you can make a template, add parts, or checkout, and it may be nice to be able to view templates before they are added to the cart as a separate function.

**Fix:** Since there is currently no frontend we see no point in adding this.

8. Overall I would modify search so all of the parameters for an item in the catalog are options to search (part_id, quantity, price) in addition to type

**Fix:** Added, redid search.

9. You could possibly change the login to include the option of logging in with either email or username. (Ex: snapchat, instagram)

**Fix:** Added.

10. It appears items are keeping track of the quantity in two different places, the part_inventory table and the pc_template_parts table. If the same inventory is represented in both locations, you want to be careful that the two quantities stay in sync with each other. In the case that there are two different inventories, one for templates and one for the general catalog, I would still recommend adding ledgers for both for the reasons suggested above.

**Fix:** That was added for future ledgerization. However since we don't recieve a quantity (we basically just add a random number of each part), it is difficult to find a reason to ledgerize the database.

11. Review whether or not all values in the tables are nullable. For example you should change the name in part_inventory to be not nullable.

**Fix:** We went through and changed columns to non nullable if they did not need to be nullable.

12. The API specs are not accurately reflected in the current code. This is seen in sign_up, the specs say only the ID is returned, whereas the code returns a message with whether or not the signup was successful.

**Fix:** Updated.

### Jinrong Pettit

1. Consider moving the login endpoints to the top of the endpoints page since that is usually the first endpoint someone would use

**Fix:** We moved this

2. Update the API specs documentation as it does not accurately reflect the current endpoints. A lot of the routes and parameters on the documentation does not accurately reflect the current codebase

**Fix:** We will update APIspec.MD to accurately reflect our codebase

3. Some tables have part_id as null and some have it as not null. Make sure that part_id is not null in all the tables

**Fix:** We fixed all null contstraint issues

4. Consider adding a password field in the users table but make sure to store the password as hashes to protect the user’s data

**Fix:** Using OAuth

5. Customer address, phone, and email should not be displayed. That data should be protected through encryption

**Fix:** We do not deem this necessary.

6. The user table and the customer table have a lot of overlap between each other. I would combine the two tables in order to simplify the data model.

**Fix:** We are not going to combine these. A user should not have to have things such as address, unless they buy something in which they become a customer.

7. Core_clock and boost_clock columns in cpu should have the float types and not integer or real

**Fix:** They do already

8. Consider adding APIs that delete an item that was added to pc_template_parts if users no longer want that particular pc part

**Fix:** This is a great point, we will add a function to do this

9. The name and type for part_inventory table should not be null and instead be not nullable

**Fix:** Already fixed all null constraint issues

10. Quantity in cart_items table should not be a bigint only ids should be just an int

**Fix:** This is already an int4

11. For monitor_specs, the data in the JSON currently has resolution as a list but in the table resolution is a string. Should convert the data in the JSON to a string since it’s not best practice to store lists in tables

**Fix:** We are not changing this

12. 3.4 Checkout Cart in API specs requests a bunch of payment information in the parameter, but it’s nowhere to be found in the codebase. It should just be gotten rid of in order to focus on simplicity.

**Fix:** We will fix APIspecs.MD to accurately reflect our codebase

13. Consider using ledgers in your database to update the amount of quantity for each item in inventory. This helps allow you to gain a history of the inventory changes over time and can track transactions

**Fix:** We will put htis under consideration if we have the time.

### Mio Nakagawa

1. The prices seem to be both int and doubles, so maybe make that consistent to double

**Fix:** Changed prices to 2 int columns (dollars and cents)

2. No null option for quantity in cart_items

**Fix:** Fixed this

3. No null for part_id

**Fix:** Fixed this

4. Do the specs in the table case_specs have an option for being null because it’s optional? If not make it not null. The same goes for the monitor_specs table

**Fix:** Some of the columns have null values in the dataset, so null is necessary for these

5. Maybe add constraints to description such as color so that what they input is actually a color

**Fix:** Users can only sell items that we have data for, so no user will ever input a color

6. Maybe add ledgers to log history and transactions

**Fix:** We do log purchase history

7. For variables/columns such as type or panel_type, maybe use enumerated types as there are probably a limited number of types or panel types

**Fix:** We feel as though it is better for users to be able to see exactly what types and panel_types parts have

8. Potentially add a password field for the user table

**Fix:** Using OAuth

9. Maybe add encryption for passwords

**Fix:** Using OAuth

10. Not exactly sure where customer_selling_id is created

**Fix:** We are not sure what this is referncing

11. Maybe add paginations for the future when the database becomes large

**Fix:** Doing this

12. Quantity maybe should be an int instead of big int just because a great amount of quantity could be problematic

**Fix:** Fixed this

## Product Ideas

### Suhanth Alluri
1. Build showcase Endpoint - 

**Response**: We don't have a frontend at the moment, so we are going to ignore this, but good idea for a future project. 

2. Comparison Endpoint 

**Response**: If we have time, we may implement this, but it can be very complex to make this happen. Working on fixing bugs first. 


### Mio Nakagawa
1. Maybe add an endpoint to see if the item is in a usable state/not broken before the user can sell the item so that the users who purchase those items will be able to use those items without any issues.

**Response:** Sellers would have to offer full refunds of items if they don't meet the standards of the users, so this endpoint woud be unnecessary

2. Maybe add an endpoint for filtering through the catalog so that the users can see what items are available.

**Added:** We have added this feedback to our search endpoint

### Hallie Christopherson

1. Experience Level: it could be helpful to have ratings on templates so someone brand new to building a pc can see a catalog that has lower complexity parts, whereas someone with more knowledge would be able to view catalogs based on their experiences.

**Response:** This is a good idea for the future, however is not currently needed. Currently will not add.

2. Reviews/Feedback: It would be cool if users could leave reviews/feedback based on their experiences with a template or product. This would be helpful as users could see more detailed feedback on templates and items. This could also be simplified by simply providing a rating with three options and an overall score as seen in the potion shop rather than providing written reviews.

**Response:** Similar to number 1, it is a good idea, however is not a top priority to add at the moment.

### Jinrong Pettit

1. As a customer looking to update only my video card, I want an endpoint that returns all of the PC parts by a certain type. Right now the catalog only returns all the PC parts that are in the catalog and there are options to return by a certain column

**Added:** We added these ideas to the search endpoint

2. As a customer who wants to build a budget PC, I would want all the PC parts that are on the cheaper side. Add an endpoint that would allow the user to sort the catalog by the category of their choice, in this case, it would be sorted by price.

**Added:** After redoing our search endpoint, it now has this functionality to search for PC parts and order by price.

## Test Results

### Checkout Errors

A common error that most reviewers ran into was an Internal Server Error during checkout. However after reviewing each reviewers `Test Results.md` we found that all errors were due to mistakes in the reviewers inputs, due to confusion on how to use the endpoint (no comments were initally made for the endpoint). The error that almost all reviewers ran into was using the wrong id during `set_item_quantity`. The endpoint was slightly confusing as depending on which catalog the user bought from, they would use a different id, so the input was called `part_id` however if it was a user item the function expected the `id` as an input. The user catalog returns:

```
[
  {
    "id": 6,
    "name": "MSI Optix G24C4",
    "type": "monitor",
    "part_id": 19840,
    "quantity": 3,
    "price": 0,
    "user_id": 6
  }
]
```

In order to make it less confusing, we added a comment to the function that states "For a user_item, make sure to use the id instead of the part_id".

### Search Error

The only other error that reviewers ran into was an internal service error when searching for an item that does not exist. We did a complete overhaul of our search endpoint and there are no longer any internal service errors that we could find during testing.