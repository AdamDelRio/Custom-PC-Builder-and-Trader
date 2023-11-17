Used data from https://github.com/docyx/pc-part-dataset grabbing from PCPartPicker.com. We used json_to_db.py to insert parts into our dataset. 

# Add Item to Cart and Purchase

Gerald (who already has an account) wants to buy a new cpu to upgrade his set up. To do this, he has two options. He can either:

## 1. Buy From The Customer PC Builder & Trader Market

1. Creates account using `/account/login`

**Input**
```json=
{
    "username":"GDawg"
}
```

**Curl**
```curl=
curl -X 'POST' \
  'https://custom-pc-builder-and-trader.onrender.com/account/login?username=GDawg' \
  -H 'accept: application/json' \
  -H 'access_token: c0d0e3ec83aa1d63f1e548125436f0a5' \
  -d ''
```

**Response**
```json=
{
  "message": "Login successful",
  "id": 10
}
```



2. Calls `GET /catalog` to view the available cpus in the Custom PC Builder market.

**Curl:**

```curl=
curl -X 'GET' \
  'https://custom-pc-builder-and-trader.onrender.com/catalog/' \
  -H 'accept: application/json'
```

**Response:**

```json=
[
  {
    "name": "AMD Ryzen 5 5600X",
    "type": "cpu",
    "part_id": 33,
    "quantity": 1,
    "price": 159.99
  }
]
```

3. After finding an item he wants, he clicks add item to cart and choosing an amount he wants, which inherintly calls `POST /carts` to get a new cart id, then calls `PUT /carts/{cart_id}/items/{part_id}` to add the item to the cart. This will also inherintly define `user_item` as `FALSE`.

## Create Cart
**Input**
```json=
{
  "user_id": 10,
  "name": "Gerald",
  "address": "1 Grand Ave",
  "phone": "696-969-6969",
  "email": "GDawg@yahoo.com"
}
```

**Curl**
```curl=
curl -X 'POST' \
  'https://custom-pc-builder-and-trader.onrender.com/carts/' \
  -H 'accept: application/json' \
  -H 'access_token: c0d0e3ec83aa1d63f1e548125436f0a5' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": 10,
  "name": "Gerald",
  "address": "1 Grand Ave",
  "phone": "696-969-6969",
  "email": "GDawg@yahoo.com"
}'
```
**Response**
```json=
{
  "cart_id": 17
}
```
## Adding item to cart
**Input**
```json=
{
    "cart_id":17,
    "part_id":33,
    "quantity":1,
    "user_item":false
}
```

**curl**
```curl=
curl -X 'POST' \
  'https://custom-pc-builder-and-trader.onrender.com/carts/17/items/33' \
  -H 'accept: application/json' \
  -H 'access_token: c0d0e3ec83aa1d63f1e548125436f0a5' \
  -H 'Content-Type: application/json' \
  -d '{
  "quantity": 1,
  "user_item": false
}'
```
**response**
```"OK"```
4. Lastly, he clicks checkout, which calls `POST /carts/{cart_id}/checkout` to purchase the item

**input**
```json=
{
    "cart_id":17,
    "payment":"credit"
}```

**curl**
```curl=
curl -X 'POST' \
  'https://custom-pc-builder-and-trader.onrender.com/carts/17/checkout' \
  -H 'accept: application/json' \
  -H 'access_token: c0d0e3ec83aa1d63f1e548125436f0a5' \
  -H 'Content-Type: application/json' \
  -d '{
  "payment": "credit"
}'
```
**response**
```json=
{
  "total_items_bought": 1,
  "total_dollars_paid": 159.99
}
```


## 2. Buy From The User Market


1. If Gerald has a user he would like to buy from he can call Calls `GET /user_catalog/{user_id}` to view the available cpus from that specific user, otherwise he can just call `GET /user_catalog` to get all the cpus offered on the user market.

2. After finding an item he wants, he clicks add item to cart and choosing an amount he wants, which inherintly calls `POST /carts` to get a new cart id, then calls `PUT /carts/{cart_id}/items/{user_parts_id}` to add the item to the cart. This will also inherintly define `user_item` as `TRUE`.

3. Lastly, he clicks checkout, which calls `POST /carts/{cart_id}/checkout` to purchase the item

# Testing Results

### Calling Catalog of Available Parts

**Curl:**

```curl
curl -X 'GET' \
  'https://custom-pc-builder-and-trader.onrender.com/user_catalog' \
  -H 'accept: application/json'
```

**Response:**

```
[
  {
    "id": 1,
    "name": "Corsair 4000D Airflow",
    "type": "case",
    "part_id": 1388,
    "quantity": 1,
    "price": 1,
    "user_id": 1
  }
]
```

### Calling Create Cart

**Curl:**

```curl
curl -X 'POST' \
  'https://custom-pc-builder-and-trader.onrender.com/carts/' \
  -H 'accept: application/json' \
  -H 'access_token: c0d0e3ec83aa1d63f1e548125436f0a5' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Gerald",
  "address": "1 Grand Ave",
  "phone": "696-969-6969",
  "email": "GDawg@yahoo.com"
}'
```

**Response:**

```
{
  "cart_id": 6
}
```

### Setting Item Quantity

**Curl:**

```curl=
curl -X 'POST' \
  'https://custom-pc-builder-and-trader.onrender.com/carts/6/items/1' \
  -H 'accept: application/json' \
  -H 'access_token: c0d0e3ec83aa1d63f1e548125436f0a5' \
  -H 'Content-Type: application/json' \
  -d '{
  "quantity": 1,
  "user_item": true
}'
```

**Response**

```
"OK"
```


### Checking Out

**Curl:**

```curl=
curl -X 'POST' \
  'http://127.0.0.1:3000/carts/6/checkout' \
  -H 'accept: application/json' \
  -H 'access_token: c0d0e3ec83aa1d63f1e548125436f0a5' \
  -H 'Content-Type: application/json' \
  -d '{
  "payment": "Credit"
}'
```


**Response:**
```
{
  "total_items_bought": 1,
  "total_dollars_paid": 1
}
```

# Create New Template

Jessica wants to create a new template for building a PC.

1. Jessica creates an account by calling `POST /account/create` and returns successful account creation.

2. She then logs into her account by calling `POST /account/login` and returns a successful login

3. She chooses to create a new PC template, so she calls `POST /template/new` and returns the template id - 4

4. She looks at the catalog of parts by calling `POST /catalog`

5. She then adds the items she wants to add parts to her template, calling `POST /templates/{user_id}/{template_id}/items/{part_id}` where `{part_id}` is the item she wants to add

6. Next, she converts her template to a cart, by clicking "Add All Items To Cart" and calls `POST /template/4/cart/new` returning a cart_id of 908

7. Finally, she purchases all of the items by clicking checkout, which call `POST /carts/908/checkout`

## Testing Results

### Creating Account

**Curl:**

```curl=
curl -X 'POST' \
  'https://custom-pc-builder-and-trader.onrender.com/account/create?username=Jessica&email=Jess%40hotmail.com' \
  -H 'accept: application/json' \
  -H 'access_token: c0d0e3ec83aa1d63f1e548125436f0a5' \
  -d ''
```

**Response:**

```json=
{
  "message": "User signed up successfully",
  "id": 6
}
```

### Logging In to Account

**Curl:**

```curl=
curl -X 'POST' \
  'https://custom-pc-builder-and-trader.onrender.com/account/login?username=Jessica' \
  -H 'accept: application/json' \
  -H 'access_token: c0d0e3ec83aa1d63f1e548125436f0a5' \
  -d ''
```

**Response:**

```json=
{
  "message": "Login successful",
  "id": 6
}
```

### Creating New Template

**Curl:**

```curl=
curl -X 'POST' \
  'https://custom-pc-builder-and-trader.onrender.com/templates/template/new' \
  -H 'accept: application/json' \
  -H 'access_token: c0d0e3ec83aa1d63f1e548125436f0a5' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": 6
}'
```

**Response:**

```json=
4
```

### Calling Catalog

**Curl:**

```curl=
curl -X 'GET' \
  'https://custom-pc-builder-and-trader.onrender.com/catalog/' \
  -H 'accept: application/json'
```

**Response:**

```json=
[
  {
    "name": "Acer B277 bmiprx",
    "type": "monitor",
    "part_id": 23933,
    "quantity": 1,
    "price": 199
  }
]
```

### Adding to Template

**Curl:**

```curl=
curl -X 'POST' \
  'https://custom-pc-builder-and-trader.onrender.com/templates/6/4/items/23933' \
  -H 'accept: application/json' \
  -H 'access_token: c0d0e3ec83aa1d63f1e548125436f0a5' \
  -H 'Content-Type: application/json' \
  -d '{
  "quantity": 1,
  "user_item": false
}'
```

**Response:**

```json=
"OK"
```

### Converting Template to Cart

**Curl:**

```curl=
curl -X 'POST' \
  'https://custom-pc-builder-and-trader.onrender.com/templates/4/cart/new' \
  -H 'accept: application/json' \
  -H 'access_token: c0d0e3ec83aa1d63f1e548125436f0a5' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": 6,
  "name": "Jessica",
  "address": "123 falala road",
  "phone": "988-475-0948",
  "email": "Jess@mial.yeet"
}'
```


**Response:**

```json=
{
  "cart_id": 16
}
```

### Purchasing Item(s)

**Curl:**

```curl=
curl -X 'POST' \
  'https://custom-pc-builder-and-trader.onrender.com/carts/16/checkout' \
  -H 'accept: application/json' \
  -H 'access_token: c0d0e3ec83aa1d63f1e548125436f0a5' \
  -H 'Content-Type: application/json' \
  -d '{
  "payment": "Gold"
}'
```

**Response:**

```json=
{
  "total_items_bought": 1,
  "total_dollars_paid": 199
}
```

# Create Account & List Item for Sale
Jimmy (who doesn't have an account) would like ot sell his old monitor, the MSI Optix G24C4. 

He does the following steps:

1. Jimmy starts by calling `POST` `/account/create` and passes in his username and email. The email will redirect to an OAuth and assume that the login was successful.

**Input:**
```json=

    {
        "username":"Jimmy"
        "email":"jimmy@gmail.com"
    }
```

**Curl:**
```curl=
curl -X 'POST' \
  'https://custom-pc-builder-and-trader.onrender.com/account/create?username=Jimmy&email=jimmy%40gmail.com' \
  -H 'accept: application/json' \
  -H 'access_token: c0d0e3ec83aa1d63f1e548125436f0a5' \
  -d ''
```

**Response**
```json=
{
  "message": "User signed up successfully",
  "id": 8
}
```
2. Jimmy searches up his part's id by using `/catalog/search`. He has a 

**Input:**

```json=
{
    "name": "MSI Optix G24C4",
    "type": "monitor"
}
```

**Curl:**
```curl=
curl -X 'POST' \
  'https://custom-pc-builder-and-trader.onrender.com/catalog/search' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "MSI Optix G24C4",
  "type": "monitor"
}'
```

**Response:**
```json=
{
  "name": "MSI Optix G24C4",
  "type": "monitor",
  "part_id": 19840,
  "quantity": 0,
  "price": 181.15
}
```

3. With a `user_id` = 8, Jimmy can go to catalog and add a part under his `user_id` using `/user_catalog/add`

**Input:**
```json=
{

  "user_id": 8,
  "part_id": 19840,
  "quantity": 1,
  "price": 125

}
```
**Curl:**
```curl=
curl -X 'POST' \
  'https://custom-pc-builder-and-trader.onrender.com/user_catalog/add' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": 8,
  "part_id": 19840,
  "quantity": 1,
  "price": 125
}'
```

**Response:**
```json=
{
  "status": "success",
  "message": "Items added/updated in user's catalog"
}

```

Done!
