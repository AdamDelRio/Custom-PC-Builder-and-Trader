# Example workflow
Gerald (who already has an account) wants to buy a new cpu to upgrade his set up. To do this, he:

Logs in to his existing account by calling POST /account/login and returns a successful login

1.) Then, he calls GET /catalog to view the available cpus

After finding one he wants, he clicks add item to cart, which inherintly calls POST /carts to get a new cart id, then calls PUT /carts/{cart_id}/items/{item_sku} to add the item to the cart

Lastly, he clicks checkout, which calls POST /carts/{cart_id}/checkout to purchase the item

# Testing results

```curl
curl -X 'GET' \
  'http://127.0.0.1:8000/catalog/' \
  -H 'accept: application/json'
```

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


```
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

```
{
  "cart_id": 6
}
```
