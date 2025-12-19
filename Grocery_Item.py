class grocery_item:
    def __init__(self, name: str, weight_or_count: float,units: str, category: str = None, item_id: int = None):
        self.name = name
        self.category = category
        self.weight_or_count = weight_or_count
        self.units = units
        self.item_id = item_id # Database primary key
