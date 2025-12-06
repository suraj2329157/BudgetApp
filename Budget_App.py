from distutils.command.check import check



class Category:
    def __init__(self, category):
        self.category = category
        self.ledger = []

    def deposit(self, amount, description = ''):
        self.ledger.append({'amount': amount, 'description': description})


    def withdraw(self, amount, description = ''):
        if self.check_funds(amount):
            self.ledger.append({'amount': -amount, 'description': description})
            return True
        return False

    def get_balance(self):
        total = 0
        for i in self.ledger:
            total += i['amount']
        return total

    def transfer(self, amount, budget_category):
        if self.check_funds(amount):
            self.withdraw(amount, f'Transfer to {budget_category.category}')
            budget_category.deposit(amount, f'Transfer from {self.category}')
            return True
        return False

    def check_funds(self,amount):
        current_balance = self.get_balance()
        return current_balance >= amount

    def __str__(self):
        length_of_heading = len(self.category)
        total_number_of_asteriks = 30 - length_of_heading
        asterisk_on_one_side = total_number_of_asteriks // 2
        heading = ''
        if asterisk_on_one_side * 2 == total_number_of_asteriks:
            for i in range(asterisk_on_one_side):
                heading += '*'
            heading += self.category
            for i in range(asterisk_on_one_side):
                heading += '*'
            heading += '\n'
        else:
            for i in range(asterisk_on_one_side):
                heading += '*'
            heading += self.category
            for i in range(asterisk_on_one_side + 1):
                heading += '*'
            heading += '\n'

        body = []
        for expenses in self.ledger:
            item = ''
            description = expenses['description'][:23]
            amount = f"{expenses['amount']:.2f}"
            no_of_spaces = 30 - len(description) - len(amount)
            item += description + ' ' * no_of_spaces + amount
            body.append(item)
        body = '\n'.join(body)
        total = f"Total: {self.get_balance():.2f}"
        display = heading + body + '\n' + total
        return display


def create_spend_chart(categories):
    total_category_expenses = []
    total_expense = 0
    for category in categories:
        category_expense = 0
        for expenses in category.ledger:
            if expenses['amount'] < 0:
                category_expense += expenses['amount']

        category_expense = -category_expense
        total_expense += category_expense
        total_category_expenses.append({'category' : category.category, 'expense': category_expense})

    percentage_category_expense = []
    for category in total_category_expenses:
        percentage = (category['expense']*100)/total_expense
        if percentage < 100 and percentage > 90:
            percentage = 90
        elif percentage < 90 and percentage > 80:
            percentage = 80
        elif percentage < 80 and percentage > 70:
            percentage = 70
        elif percentage < 70 and percentage > 60:
            percentage = 60
        elif percentage < 60 and percentage > 50:
            percentage = 50
        elif percentage < 50 and percentage > 40:
            percentage = 40
        elif percentage < 40 and percentage > 30:
            percentage = 30
        elif percentage < 30 and percentage > 20:
            percentage = 20
        elif percentage < 20 and percentage > 10:
            percentage = 10
        elif percentage < 10 and percentage > 0:
            percentage = 0
        percentage_category_expense.append({'category': category['category'], 'percentage': percentage})
    bar_chart = ['Percentage spent by category']
    bar_levels = [100,90,80,70,60,50,40,30,20,10,0]
    for level in bar_levels:
        line = ''
        for i in range(3,len(str(level)),-1):
            line += ' '
        line += str(level) + '|'
        for category in percentage_category_expense:
            if category['percentage'] >= level:
                line += ' o '
            else:
                line += '   '
        line += ' '
        bar_chart.append(line)

    line = '    '
    for _ in range(len(categories)):
        line += '---'
    line += '-'
    bar_chart.append(line)

    maximum_lines = len(categories[0].category)
    for i in range(1,len(categories)):
        if maximum_lines < len(categories[i].category):
            maximum_lines = len(categories[i].category)


    for i in range(maximum_lines):
        line = ''
        line += '    '
        for category in categories:
            if i < len(category.category):
                line += ' ' + category.category[i] + ' '
            else:
                line += '   '
        line += ' '
        bar_chart.append(line)

    bar_chart = '\n'.join(bar_chart)

    return bar_chart







food = Category('Food')
food.deposit(1000, 'deposit')
food.withdraw(10.15, 'groceries')
food.withdraw(15.89, 'restaurant and more food for dessert')
clothing = Category('Clothing')
food.transfer(50, clothing)
clothing.withdraw(40,'winter clothes')
print(food)
categories = [food, clothing]
print()
print(create_spend_chart(categories))
