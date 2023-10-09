## User Stories


## Exceptions

**1. Credit card declined**
- If a credit card gets declined, we will return an error to the user to resubmit another payment method. The cart will not be emptied yet, and the order will still be pending.
**2. Invalid shipping address**
- If an invalid shipping address, we will prompt a warning to the user that the shipping address doesn’t match with USPS (or another address checker). Give the option to fix the address or continue with their inputted address (with a warning). 
**3. Searching for something not in the database**
- Return no exact results and show other similar results that the customer might be interested in. 
**4. Uploading something not in the database**
- Create a new item for the part after admin approval of product specs and information. 
**5. Listing an item for a trade you do not own**
Delist and refund payment to the customer. 
**6. Trying to add an incompatible part**
- Add a warning of an incompatible part with a reason why it’s incompatible. Show other parts that would be compatible instead to swap. 
**7. The database is not responding/connecting**
- The website front down to a 404 page and prompts the database to start up again. Push devs to debug what is going on. 
**8. Multiple requests for a part that has low stock - concurrency problem (who gets the item)**
- Check POST time to see who was first and go in a queue-based system??? Hard question to answer…
**9. Trying to buy something that’s out of stock**
- When at checkout, check the database and part stock. If out of stock, add them to a backorder list or send an email when in stock option.
**10. The user is not authorized**
- Trying to access an admin page will prompt an error message and redirect to the home directory
**11. The user is trying to access a non-existent page**
- 404 error page and redirect back to home. 
**12. The user is not logged in**
- Prompt user to login before checking out with cart, or add a guest feature with phone number and email without creating an account. 
