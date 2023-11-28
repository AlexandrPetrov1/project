import csv

with open('iphone.csv', 'r', newline='') as file:
    reader = csv.reader(file, delimiter=';')
    next(reader)

    cheapest_price = float('inf')
    cheapest_phone = ""

    for row in reader:
        phone_name = row[0]
        memory = row[1]
        price = float(row[2])

        if price < cheapest_price:
            cheapest_price = price
            cheapest_phone = (phone_name, memory, price)


print(f'Самая низкая цена: "{cheapest_phone[2]}" у телефона: "{cheapest_phone[0]}" с памятью: "{cheapest_phone[1]} GB"')