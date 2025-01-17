class Category:

    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        total_balance = sum(item["amount"] for item in self.ledger)
        return total_balance

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        return self.get_balance() >= amount

    def __str__(self):
        title = self.name.center(30, '*') + "\n"
        items = ""
        for item in self.ledger:
            desc = item["description"][:23].ljust(23)
            amt = f"{item['amount']:.2f}".rjust(7)
            items += f"{desc}{amt}\n"
        total = f"Total: {self.get_balance():.2f}"
        return title + items + "\n" + total


def create_spend_chart(categories):
    total_spent = 0
    category_spending = []

    for category in categories:
        spent = sum(-item["amount"] for item in category.ledger if item["amount"] < 0)
        category_spending.append(spent)
        total_spent += spent

    percentages = [int((spent / total_spent) * 100) for spent in category_spending]

    chart = "Percentage spent by category\n"

    for i in range(100, -1, -10):
        chart += str(i).rjust(3) + "| "
        for percentage in percentages:
            if percentage >= i:
                chart += "o  "
            else:
                chart += "   "
        chart += "\n"

    chart += "    -" + "---" * len(categories) + "\n"

    max_name_length = max(len(category.name) for category in categories)
    for i in range(max_name_length):
        chart += "     "
        for category in categories:
            if i < len(category.name):
                chart += category.name[i] + "  "
            else:
                chart += "   "
        chart += "\n"

    return chart.strip()


# User Input for Categories and Transactions
categories = {}
while True:
    category_name = input("Enter the category name (or 'done' to finish, 'exit' to quit): ").strip().lower()
    if category_name == 'done':
        break
    if category_name == 'exit':
        print("Program exited.")
        exit()  # Terminate the program if 'exit' is entered
    if category_name not in categories:
        categories[category_name] = Category(category_name)

    while True:
        transaction_type = input("Enter transaction type (deposit, withdraw, transfer, 'done' to finish category, 'exit' to quit): ").strip().lower()
        if transaction_type == 'done':
            break
        if transaction_type == 'exit': 
            print("Exiting the program.") 
            exit()
        amount = float(input("Enter the amount: "))
        description = input("Enter the description: ").strip()

        if transaction_type == 'deposit':
            categories[category_name].deposit(amount, description)
        elif transaction_type == 'withdraw':
            categories[category_name].withdraw(amount, description)
        elif transaction_type == 'transfer':
            destination_category = input("Enter the destination category: ").strip().lower()
            if destination_category not in categories:
                categories[destination_category] = Category(destination_category)
            categories[category_name].transfer(amount, categories[destination_category])

# Display Category Ledgers
for category in categories.values():
    print(category)

# Create Spending Chart
print(create_spend_chart(list(categories.values())))
