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
