"""
Supply Chain Inventory Tracker

Class: SupplyChainInventory

Problem Statement:
You are building a Supply Chain Inventory Tracker for a retail chain. Each product
has a Product ID (unique string) and Units in stock (integer). The system manages
inflow and outflow of goods and offers utilities to manage restocking and listing items in stock.

State Initialization:
def __init__(self):
    self.inv = {}

Methods Required:
1. add_product(self, product_id: str, quantity: int) -> dict
   If product ID exists, increase quantity; otherwise create entry. Return updated dictionary.
2. fulfill_order(self, product_id: str, quantity: int) -> dict
   If existing stock < quantity or product not found, raise ValueError("Insufficient Stock").
   Otherwise subtract quantity. Return updated dictionary.
3. restock_return(self, product_id: str, quantity: int) -> dict
   Add returned quantity back to product ID or create entry. Return updated dictionary.
4. list_available_products(self) -> list
   Return list of product IDs where stock > 0.
"""


class SupplyChainInventory:
    def __init__(self):
        self.inv = {}

    def add_product(self, product_id: str, quantity: int) -> dict:
        if product_id in self.inv:
            self.inv[product_id] += quantity
        else:
            self.inv[product_id] = quantity
        return self.inv

    def fulfill_order(self, product_id: str, quantity: int) -> dict:
        if product_id not in self.inv or self.inv[product_id] < quantity:
            raise ValueError("Insufficient Stock")
        self.inv[product_id] -= quantity
        return self.inv

    def restock_return(self, product_id: str, quantity: int) -> dict:
        if product_id in self.inv:
            self.inv[product_id] += quantity
        else:
            self.inv[product_id] = quantity
        return self.inv

    def list_available_products(self) -> list:
        return [product_id for product_id, stock in self.inv.items() if stock > 0]


if __name__ == "__main__":
    tracker = SupplyChainInventory()
    print("Add ProductB (10):", tracker.add_product("ProductB", 10))
    print("Add ProductC (25):", tracker.add_product("ProductC", 25))
    print("Fulfill Order ProductB (6):", tracker.fulfill_order("ProductB", 6))
    print("Restock Return ProductB (5):", tracker.restock_return("ProductB", 5))
    print("Available Products:", tracker.list_available_products())
