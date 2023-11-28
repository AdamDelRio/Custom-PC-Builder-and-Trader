# Concurrency Issues


## Case 1: Non-Repeatable Read

If a customer checks the customer catalog for a specific part, then adds the item to cart, they could encounter a non-repeatable read. For instance, say a customer checks the catalog, and right after that the user that made the listing changes the price of their item. The customer will try and check out with the old price, and thus there is a concurrency issue.

This scenario can be resolved by increasing the isolation level to REPEATABLE READ.

![sequenceDiagram1](https://hackmd.io/_uploads/BJsizqMBT.png)

## Case 2: Write Skew / Lost Update

If two customers are checking out concurrently, but buying the same product, they will encounter a lost update, which is a form of a write skew. Say there is only 3 monitors in stock of the same type, and customer A wants to buy 3, while customer B wants to buy 1. No matter who checks out first, the second customer will not be able to purchase their desired quantity. 

This scenario can be resolved by increasing the isolation level to SERIALIZABLE

![untitled](https://hackmd.io/_uploads/SyKoWkEST.png)


## Case 3: Non-Repeatable Read

If a customer sees in the user catalog that a user is selling a motherboard that is significantly undervalued, they may want to buy all of them to resell. When they call the catalog, say there is three in stock. As they go to check out with all three motherboards, the user adds one more motherboard to the catalog. Now, the customer only has three to sell when they could have maximized their profits by buying all four. This is a non-repeatable read scenario.

This issue could be resolved by increasing the isolation level to REPEATABLE READ.

![Screenshot 2023-11-27 142017](https://hackmd.io/_uploads/r1HxPczSa.png)



