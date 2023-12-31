def read_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            fields = line.strip().split(',')
            data.append((fields[0].strip(), float(fields[1].strip())))
    return data


def calculate_totals(check, product_list):
    total_shopping_amount = 0.0
    roommate_due = 0.0
    not_found_products = []

    check_dict = {product: {'price': price, 'quantity': 0} for product, price in check}

    for product, unit_price in check:
        quantity = 1
        total_shopping_amount += unit_price * quantity
        check_dict[product]['quantity'] += quantity

    for product, quantity in product_list:
        if product in check_dict and check_dict[product]['quantity'] > 0:
            check_dict[product]['quantity'] -= int(quantity)
        else:
            not_found_products.append((product, quantity))

    for product, info in check_dict.items():
        roommate_due += info['price'] * info['quantity']

    return total_shopping_amount, roommate_due, not_found_products


def check_taken(product_list, check_dict):
    taken_items = [(product, min(quantity, check_dict[product]['quantity']), check_dict[product]['price']) for product, quantity in product_list if product in check_dict and check_dict[product]['quantity'] > 0]

    with open('taken_items.txt', 'w') as file:
        for product, quantity, price in taken_items:
            file.write(f"{product} (Requested: {quantity}, Taken: {check_dict[product]['quantity']}): ${price * quantity:.2f}\n")


def calculate_payment_amount(taken_items_file):
    total_payment_amount = 0.0

    with open(taken_items_file, 'r') as file:
        for line in file:
            parts = line.split(': $')
            if len(parts) == 2:
                product_info, price_str = parts
                product, requested_quantity, taken_quantity = parse_product_info(product_info)
                price = float(price_str)
                total_payment_amount += price

    return total_payment_amount


def parse_product_info(product_info):
    parts = product_info.strip().split('(Requested: ')
    if len(parts) == 2:
        product, quantities = parts
        requested_str, taken_str = quantities.split(', Taken: ')
        requested_quantity = int(float(requested_str))
        taken_quantity = int(taken_str[:-1])  # Remove the closing parenthesis
        return product, requested_quantity, taken_quantity
    else:
        return None, 0, 0


def main():
    check_file_path = 'check.txt'
    product_list_file_path = 'product_list.txt'

    check = read_file(check_file_path)
    product_list = read_file(product_list_file_path)

    total_shopping_amount, roommate_due, not_found_products = calculate_totals(check, product_list)
    check_dict = {product: {'price': price, 'quantity': 0} for product, price in check}
    for product, unit_price in check:
        quantity = 1
        check_dict[product]['quantity'] += quantity

    check_taken(product_list, check_dict)

    taken_items_file_path = 'taken_items.txt'
    total_payment = calculate_payment_amount(taken_items_file_path)
    print(f"Total amount of shopping: ${total_shopping_amount:.2f}")
    print(f"Total due from roommate: ${total_payment:.2f}")

    if not_found_products:
        print("\nProducts not found in the check:")
        for product, quantity in not_found_products:
            print(f"{product}: {int(quantity)}")


main()
