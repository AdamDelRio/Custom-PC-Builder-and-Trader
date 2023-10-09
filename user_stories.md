## User Stories

- As a customer, I want a new monitor to play League of Legends
- As a customer, I want to trade in my old GPU for cash to purchase a new one
- As a user, I want to research which GPU would be compatible with my current setup
- As a customer, I want to purchase a new graphics card that is compatible with my PC
- As a trader, I am looking to trade a CPU I bought for a GPU that is compatible with my PC
- As a user, I just want to see what parts I could afford to build a PC within my current budget
- As a customer, I am looking to update my RAM with a budget of $100
- As a user, I am looking to see how much it would cost to upgrade my hard drive
- As a streamer, I want PC parts that are powerful enough to support streaming and gaming
- As an editor, I need to make sure that the parts I buy are capable of performing all of my needs
- As a software developer, I want to plan out and purchase a dual-monitor setup to have a more efficient workflow. 
- As a student, I want to build a budget-friendly PC for educational purposes and light gaming

## Exceptions

- Credit card declined
  - If a credit card gets declined, we will return an error to the user to resubmit another payment method. The cart will not be emptied yet, and the order will still be pending.

- Invalid shipping address
  - If an invalid shipping address, we will prompt a warning to the user that the shipping address doesn’t match with USPS (or another address checker). Give the option to fix the address or continue with their inputted address (with a warning). 

- Searching for something not in the database
  - Return no exact results and show other similar results that the customer might be interested in.
  
- Uploading something not in the database
  - Create a new item for the part after admin approval of product specs and information.
  
- Listing an item for a trade you do not own
  - Delist and refund payment to the customer.
  
- Trying to add an incompatible part
  - Add a warning of an incompatible part with a reason why it’s incompatible. Show other parts that would be compatible instead to swap.

- The database is not responding/connecting
  - The website front down to a 404 page and prompts the database to start up again. Push devs to debug what is going on.
  
- Multiple requests for a part that has low stock - concurrency problem (who gets the item)
  - Check POST time to see who was first and go in a queue-based system??? Hard question to answer…
  
- Trying to buy something that’s out of stock
  - When at checkout, check the database and part stock. If out of stock, add them to a backorder list or send an email when in stock option.
  
- The user is not authorized
  - Trying to access an admin page will prompt an error message and redirect to the home directory

- The user is trying to access a non-existent page
  - 404 error page and redirect back to home.

- The user is not logged in
  - Prompt user to login before checking out with cart, or add a guest feature with phone number and email without creating an account. 
