# Example workflow
Gerald (who already has an account) wants to buy a new graphics card to upgrade his set up. To do this, he:

Logs in to his existing account by calling POST /account/login and returns a successful login
Then, he calls GET /catalog to view the available graphics card
After finding one he wants, he clicks add item to cart, which inherintly calls POST /carts to get a new cart id, then calls PUT /carts/{cart_id}/items/{item_sku} to add the item to the cart
Lastly, he clicks checkout, which calls POST /carts/{cart_id}/checkout to purchase the item

# Testing results
