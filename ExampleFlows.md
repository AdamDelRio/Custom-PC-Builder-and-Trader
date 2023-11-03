# ExampleFlows.md

# Example Flow

## 1. Create New Template

Jessica wants to create a new template for building a PC. 

1. Jessica creates an account by calling POST `/account/create` and returns successful account creation with `user id`
3. She chooses to create a new PC template, so she calls POST `/template/new` and returns the template id - `2423`
4. She looks at the catalog of parts by calling POST `/catalog`
5. She then adds the items she wants to add parts to her template, calling POST `/template/existing/2423/add_part/{part_type}/{part_id}` where `{part_type}` is the type of the item she wants to add and `{part_id}` is the id
6. Next, she converts her template to a cart, by clicking "Add All Items To Cart" and calls  POST `/template/existing/2423/add_to_cart` returning a cart_id of 908
7. Finally, she purchases all of the items by clicking checkout, which call POST `/carts/908/checkout`

## 2. Add An Item To Cart and Purchase

Gerald (who already has an account) wants to buy a new graphics card to upgrade his set up.  To do this, he:

- Logs in to his existing account by calling POST `/account/login` and returns a successful login
- Then, he calls GET `/catalog` to view the available graphics card
- After finding one he wants, he clicks add item to cart, which inherintly calls POST `/carts` to get a new cart id, then calls PUT `/carts/{cart_id}/items/{item_sku}` to add the item to the cart
- Lastly, he clicks checkout, which calls POST `/carts/{cart_id}/checkout` to purchase the item


## 3. Create an account & list item for sale

Jimmy (who does not have an account) would like to sell his old monitor. To do so he:

- starts by calling POST `/account/create` and passes in his first name, last name, email, password, address, and date of birth. This returns his customer id of 104.
- then Jimmy adds the item he would like to sell to the catalog. He calls POST `/catalog/add/104` and passes in the name of the item he is selling, the quantity, and the price.

Now Jimmy is ready to sell his item.
