# Performance Writeup

## Fake Data Modeling

Should contain a link to the python file you used to construct the million rows of data for your service. Should also contain a writeup explaining how many final rows of data you have in each of your table to get to a million rows AND a justification for why you think your service would scale in that way. There is no single right answer to this, but your reasoning must be justifiable.

**Python File For Populating Database:**
https://github.com/AdamDelRio/Custom-PC-Builder-and-Trader/blob/main/populate_posts.py

```
quants = {
    "add_users": 50000,
    "add_case_specs": 100000,
    "add_cpu_specs": 100000,
    "add_internal_hard_drive_specs": 100000,
    "add_monitor_specs": 100000,
    "add_motherboard_specs": 100000,
    "add_power_supply_specs": 100000,
    "add_video_card_specs": 100000,
    "add_user_parts": 100000,
    "add_carts_and_cart_items": 100000,
    "add_pc_templates_and_parts": 100000
}
```
We decided to fake 100,000 rows of each part type. We wanted to see how our search would perform if we offered every PC component in existence. We added 50,000 users, 100,000 carts and cart items along with 100,000 templates and template parts. In hindsight, we definitely could have added more rows in these fields, but for a few different reasons this data took a very long time to populate. Overall, we are pretty happy with how each of our endpoints performed with this abundance of data populating our database.

## Performance results of hitting endpoints

For each endpoint, list how many ms it took to execute. State which three endpoints were the slowest.

### Account

`/account/create` - 49 ms
`/account/login` - 27 ms

### Cart

`/carts/` - 50 ms
`/carts/82/items/1500` - 65 ms
`/carts/82/checkout` - 148 ms

### Catalog

`/catalog/search` - 1640 ms
`/user_catalog/add` - 78 ms
`/catalog/search_user_catalog` - 1890 ms

### Templates
`/templates/template/new` - 16 ms
`/templates/{user_id}/{template_id}/items/{part_id}` - 53 ms
`/templates/{template_id}/remove/items/{part_id}` - 22 ms
`/templates/{template_id}/cart/new` - 50 ms

## Three Slowest Endpoints:

- `/catalog/search_user_catalog`
- `/catalog/search`
- `/carts/82/checkout`

## Performance tuning

For each of the three slowest endpoints, run explain on the queries and copy the results of running explain into the markdown file. Then describe what the explain means to you and what index you will add to speed up the query. Then copy the command for adding that index into the markdown and rerun explain. Then copy the results of that explain into the markdown and say if it had the performance improvement you expected. Continue this process until the three slowest endpoints are now acceptably fast (think about what this means for your service).

### `/catalog/search_user_catalog`

**Results of Explain:**

```
Limit  (cost=17830.88..17830.88 rows=1 width=133)
  ->  Sort  (cost=17830.88..17830.88 rows=1 width=133)
        Sort Key: pi.name
        ->  Hash Right Join  (cost=14970.85..17830.87 rows=1 width=133)
              Hash Cond: (specs.part_id = up.part_id)
              ->  Seq Scan on internal_hard_drive_specs specs  (cost=0.00..2485.00 rows=100000 width=53)
              ->  Hash  (cost=14970.84..14970.84 rows=1 width=64)
                    ->  Hash Join  (cost=12624.34..14970.84 rows=1 width=64)
                          Hash Cond: (up.part_id = pi.part_id)
                          ->  Seq Scan on user_parts up  (cost=0.00..2084.00 rows=100000 width=32)
                                Filter: (quantity > 0)
                          ->  Hash  (cost=12624.30..12624.30 rows=3 width=36)
                                ->  Gather  (cost=1000.00..12624.30 rows=3 width=36)
                                      Workers Planned: 2
                                      ->  Parallel Seq Scan on part_inventory pi  (cost=0.00..11624.00 rows=1 width=36)
"                                            Filter: ((name ~~* ''::text) AND (type ~~* 'internal_hard_drive'::text))"
```

The slow performance of this query is likely due to the full table scans and the  filtering on the name and type columns in the part_inventory table. To speed up this query, we think we should add an index on these two columns to make the filtering more efficient.

**Create Index:**

```
CREATE INDEX idx_part_inventory_name ON part_inventory (name);
CREATE INDEX idx_part_inventory_type ON part_inventory (type);
```

**Explain Output After Adding Index:**

```
Limit  (cost=5292.09..5292.09 rows=1 width=133)
  ->  Sort  (cost=5292.09..5292.09 rows=1 width=133)
        Sort Key: pi.name
        ->  Hash Right Join  (cost=2432.06..5292.08 rows=1 width=133)
              Hash Cond: (specs.part_id = up.part_id)
              ->  Seq Scan on internal_hard_drive_specs specs  (cost=0.00..2485.00 rows=100000 width=53)
              ->  Hash  (cost=2432.04..2432.04 rows=1 width=64)
                    ->  Hash Join  (cost=85.54..2432.04 rows=1 width=64)
                          Hash Cond: (up.part_id = pi.part_id)
                          ->  Seq Scan on user_parts up  (cost=0.00..2084.00 rows=100000 width=32)
                                Filter: (quantity > 0)
                          ->  Hash  (cost=85.51..85.51 rows=3 width=36)
                                ->  Bitmap Heap Scan on part_inventory pi  (cost=4.58..85.51 rows=3 width=36)
"                                      Filter: ((name ~~* ''::text) AND (type ~~* 'internal_hard_drive'::text))"
                                      ->  Bitmap Index Scan on idx_part_inventory_name  (cost=0.00..4.58 rows=21 width=0)
"                                            Index Cond: (name = ''::text)"
```

Total cost was reduced from 17830.88 to 5292.09 and the query plan used efficient index usage on the part_inventory table for filtering on name and type. **Result:** Significant reduction in total cost and expected improvement in query performance.

### `/catalog/search`

**Results of Explain:**

```
Limit  (cost=16366.76..16367.00 rows=2 width=96)
  ->  Gather Merge  (cost=16366.76..16367.00 rows=2 width=96)
        Workers Planned: 2
        ->  Sort  (cost=15366.74..15366.74 rows=1 width=96)
              Sort Key: part_inventory.name
              ->  Parallel Hash Left Join  (cost=2621.54..15366.73 rows=1 width=96)
                    Hash Cond: (part_inventory.part_id = cpu_specs.part_id)
                    ->  Parallel Seq Scan on part_inventory  (cost=0.00..12745.17 rows=1 width=52)
"                          Filter: ((name ~~* ''::text) AND (type ~~* 'cpu'::text) AND (quantity > 0))"
                    ->  Parallel Hash  (cost=1886.24..1886.24 rows=58824 width=28)
                          ->  Parallel Seq Scan on cpu_specs  (cost=0.00..1886.24 rows=58824 width=28)
```

The slow performance of this query is likely due to the full table scans and the  filtering on the name and type columns in the part_inventory table. To speed up this query, we think we should add an index on these two columns to make the filtering more efficient.

**Create Index:**

```
CREATE INDEX idx_part_inventory_name ON part_inventory (name);
CREATE INDEX idx_part_inventory_type ON part_inventory (type);
```

**Explain Output After Adding Index:**

```
Limit  (cost=2646.24..2646.25 rows=3 width=96)
  ->  Sort  (cost=2646.24..2646.25 rows=3 width=96)
        Sort Key: part_inventory.name
        ->  Hash Right Join  (cost=85.69..2646.22 rows=3 width=96)
              Hash Cond: (cpu_specs.part_id = part_inventory.part_id)
              ->  Seq Scan on cpu_specs  (cost=0.00..2298.00 rows=100000 width=28)
              ->  Hash  (cost=85.65..85.65 rows=3 width=52)
                    ->  Bitmap Heap Scan on part_inventory  (cost=4.58..85.65 rows=3 width=52)
"                          Filter: ((name ~~* ''::text) AND (type ~~* 'cpu'::text) AND (quantity > 0))"
                          ->  Bitmap Index Scan on name_index  (cost=0.00..4.58 rows=21 width=0)
"                                Index Cond: (name = ''::text)"
```

Total cost was reduced from 16367.00 to 2646.25 and the query plan used efficient index usage on the part_inventory table for filtering on name and type. **Result:** Significant reduction in total cost and expected improvement in query performance.

### `/{cart_id}/checkout`

**Results of Explain:**

```
Nested Loop Left Join  (cost=0.72..3543.61 rows=1 width=41)
  ->  Nested Loop Left Join  (cost=0.42..3535.28 rows=1 width=17)
        ->  Seq Scan on cart_items  (cost=0.00..3526.84 rows=1 width=9)
              Filter: ((NOT checked_out) AND (cart_id = 15))
        ->  Index Scan using part_inventory_pkey on part_inventory  (cost=0.42..8.44 rows=1 width=12)
              Index Cond: (part_id = cart_items.part_id)
  ->  Index Scan using user_parts_pkey on user_parts  (cost=0.29..8.31 rows=1 width=12)
        Index Cond: (id = cart_items.part_id)
```

The query's slow performance is likeley due to the absence of an index on the cart_id column in the cart_items table, resulting in full table scans (Seen here: ->  Seq Scan on cart_items  (cost=0.00..3526.84 rows=1 width=9)). To fix this and optimize query efficiency, an index on the cart_id column should be created.

**Create Index:**

```
CREATE INDEX cart_index ON cart_items (cart_id);
```

**Explain Output After Adding Index:**

```
Nested Loop Left Join  (cost=1.14..25.23 rows=1 width=41)
  ->  Nested Loop Left Join  (cost=0.84..16.90 rows=1 width=17)
        ->  Index Scan using cart_index on cart_items  (cost=0.42..8.46 rows=1 width=9)
              Index Cond: (cart_id = 15)
              Filter: (NOT checked_out)
        ->  Index Scan using part_inventory_pkey on part_inventory  (cost=0.42..8.44 rows=1 width=12)
              Index Cond: (part_id = cart_items.part_id)
  ->  Index Scan using user_parts_pkey on user_parts  (cost=0.29..8.31 rows=1 width=12)
        Index Cond: (id = cart_items.part_id)
```

Total cost was reduced from 3543.61 to 25.23 and the query plan used efficient index usage on the cart_items table for filtering on cart_id. **Result:** Significant reduction in total cost and expected improvement in query performance.


