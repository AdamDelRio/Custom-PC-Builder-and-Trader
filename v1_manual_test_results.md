# Example workflow

Gerald (who already has an account) wants to buy a new cpu to upgrade his set up. To do this, he:

1. Calls `GET /catalog` to view the available cpus

2. After finding one he wants, he clicks add item to cart, which inherintly calls `POST /carts` to get a new cart id, then calls `PUT /carts/{cart_id}/items/{item_sku}` to add the item to the cart

3. Lastly, he clicks checkout, which calls `POST /carts/{cart_id}/checkout` to purchase the item

# Testing results

### Calling Catalog of Available Parts

**Curl:**

```curl
curl -X 'GET' \
  'http://127.0.0.1:8000/catalog/' \
  -H 'accept: application/json'
```

**Response:**

```
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

### Calling Create Cart

**Curl:**

```curl
curl -X 'POST' \
  'http://127.0.0.1:8000/carts/' \
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
  'http://127.0.0.1:8000/carts/6/items/33' \
  -H 'accept: application/json' \
  -H 'access_token: c0d0e3ec83aa1d63f1e548125436f0a5' \
  -H 'Content-Type: application/json' \
  -d '{
  "quantity": 1
}'
```

**Response**

```
"OK"
```


### Checking Out

**Curl:**
```
curl -X 'POST' \
  'http://127.0.0.1:8000/carts/6/checkout' \
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
  "total_gold_paid": 159.99
}
```
