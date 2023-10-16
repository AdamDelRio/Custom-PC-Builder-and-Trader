# APISpec.md

# API Specification

## 1. Accounts

### 1.1 Create an account - `/account/create` - `POST`

**Request**:

```json
{
	"first_name": "string",
	"last_name": "string",
	"email": "string",
	"password": "string",
	"address": "string",
	"date_of_birth": "date"
}
```

**Returns**: 

```json
{
	"success":"boolean" /*True if created, false if error*/
}
```

### **1.2 Login to an existing account - `/account/login/` - `POST`**

**Request**:

```json
{
	"username": "string",
	"password": "string"
}
```

**Returns:**

```json
{
	"success":"boolean" /*True if logged in, false if password error*/
}
```

## 2. PC Build Templates (new and existing)

Creates a PC Build Template

Users can use any of these API calls when using/creating a PC Building Template:

1. `Create PC Template`
2. `Get Existing PC Template`

### 2.1 Create PC Template - `/template/new/` - `POST`

**Request**:

```jsx
{
	"account_id": "string"
	"visibility": "boolean" /*if True, public visibility; False, private visibility*/
}
```

**Returns**:

```jsx
{
	"template_id": "string" /* This id will be used for future calls to add items and checkout */
}
```

### 2.2 Get Existing PC Template - `/template/existing/{template_id}` - `GET`

**Returns**:

```jsx
{
	"template_catalog": "json"  /* This will include a list of the parts in the existing template
}
```

### 2.3 Convert Template to Cart - `/template/existing/{template_id}/add_to_cart` - `POST`

Creates cart if no cart under user, else creates cart and adds parts to cart

**Request:**

```json
{
	"cart_id":"string",
	"items":"json"
}
```

**Returns:**

```json
{
	"cart_id":"string"
}
```

### 2.4 Add Item to Template - `/template/existing/{template_id}/add_part/{{part_id}` - POST

Adds a PC part to an existing template and returns a true/false boolean if successful

**Request:**

```json
{
	"item_id":"string",
	"product_type":"string"
}
```

**Returns:**
```json
{
	"result":"boolean"
}
```

## 3. Customer Purchasing

The API calls are made in this sequence when making a purchase:

1. `Get Catalog`
2. `New Cart`
3. `Add Item to Cart` (Can be called multiple times)
4. `Checkout Cart`

### 3.1 Get Catalog - `/catalog/` - `GET`

Retrieves the catalog of items. Each unique item combination should have only a single price.

**Returns**:

```json
[
    {
        "sku": "string", /* Matching regex ^[a-zA-Z0-9_]{1,20}$ */
        "name": "string",
        "quantity": "integer", /* Greater than 0 */
        "price": "integer", /* Greater than 0 */
        "customer_selling_id": "string",
    }
]
```

### 3.2 New Cart - `/carts/` - `POST`

Creates a new cart for a specific customer.

**Request**:

```json
{
	"account_id": "string"
}
```

**Returns**:

```json
{
	"cart_id": "string" /* This id will be used for future calls to add items and checkout */
}
```

### 3.3 Add Item to Cart - `/carts/{cart_id}/items/{item_sku}` - `PUT`

Updates the quantity and customer selling id of a specific item in a cart.

**Request**:

```json
{
	"quantity": "integer"
	"customer_selling_id": "string"
}
```

**Returns**:

```json
{
    "success": "boolean"
}
```

### 3.4 Checkout Cart - `/carts/{cart_id}/checkout` - `POST`

Handles the checkout process for a specific cart.

**Request**:

```json
{
  	"cardholder_name": "string"
	"cc_number": "string",
  	"exp_date": "string",
  	"cvv" : "string", 
	"street_address": "string"
	"city": "string"
	"state": "string"
	"zip": "string"
}
```

**Returns**:

```json
[
	{
	    "item_sku": "string"
	    "quantity": "integer"
			"item_price": "integer"
	}
]
```

### 3.5 Clear Cart - `/carts/{cart_id}/clear` - `POST`

****************Returns:****************

```jsx
{
	"success": "boolean"
}
```

## 4. Selling

The API calls are made in this sequence for selling:

1. `Add items to customer catalog`

### 4.1 Add to catalog - `/catalog/add/{customer_id}` - `POST`

Adds items for selling to the customer's catalog, which is then added to the total catalog

**Request**:

```jsx
[
    {
        "sku": "string", /* Matching regex ^[a-zA-Z0-9_]{1,20}$ */
        "name": "string",
        "quantity": "integer", /* Greater than 0 */
        "price": "integer", /* Greater than 0 */
    }
]
```

**Returns**:

```jsx
{
	"success":"boolean" /*True if created, false if error
}
```
