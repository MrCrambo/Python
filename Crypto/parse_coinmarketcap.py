import csv

price = []
mc = []
volume = []

with open("t.txt", 'r') as txtfile:
    full = txtfile.read().split('class="sc-47a23l-0 jzTYkA">')[1:]
    for i in range(len(full) / 6):
        price.append(full[3 + i * 6].split('<')[0])
        volume.append(full[4 + i * 6].split('<')[0].replace('&nbsp;', ''))
        mc.append(full[5 + i * 6].split('<')[0].replace('&nbsp;', ''))

with open("results3.csv", "w") as csvfile:
    fieldnames = ['price', 'mc', 'volume']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(len(price) - 1, 0, -1):
        writer.writerow({'price': price[i], 'mc': mc[i], 'volume': volume[i]})