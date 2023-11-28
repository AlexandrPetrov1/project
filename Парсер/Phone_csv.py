import csv
from parser import phone_name, phone_GB, phone_price

with open("iphone.csv", 'w', newline='') as file:
    names = ["Название", "Память", "Цена"]
    writer = csv.writer(file, delimiter=';')
    writer.writerow(names)
with open("iphone.csv", 'a', newline='') as file:
    writer = csv.writer(file, delimiter=';')

    for item1, item2, item3 in zip(phone_name, phone_GB, phone_price):
        writer.writerow([item1, item2, item3])
