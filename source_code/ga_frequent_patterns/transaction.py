class CTransaction:

    def __init__(self, items, utilities, transaction_utility):
        self.items = items
        self.utilities = utilities
        self.transaction_utility = transaction_utility
        self.offset = 0
        self.prefix_utility = 0

    def __str__(self) -> str:
        return f"{self.items} : {self.transaction_utility} : {self.utilities}"

    @property
    def get_transaction_utility(self):
        return self.transaction_utility

    @property
    def get_utilities(self):
        return self.utilities

    @property
    def get_items(self):
        return self.items


if __name__ == "__main__":
    t = CTransaction(0, 0, 0)
    print(t)
