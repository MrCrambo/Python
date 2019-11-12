import csv

eth_reader = open("leo_eth.csv", "r")
eth_mc = [] # CapMrktCurUSD
eth_addrs = [] # AdrActCnt
eth_sply = [] # SplyCur
eth_price = [] # PriceUSD
eth_tx = [] # TxCnt
eth_tf_tx = [] # TxTfrCnt
eth_adj_tf = []

for line in eth_reader.readlines()[1:]:
    vals = line.split(',')
    eth_mc.append(float(vals[2]))
    eth_addrs.append(int(vals[1]))
    eth_sply.append(float(vals[11]))
    eth_price.append(float(vals[8]))
    eth_tx.append(int(vals[12]))
    eth_tf_tx.append(int(vals[13]))
    eth_adj_tf.append(float(vals[15]))


eos_reader = open("leo_eos.csv", "r")
eos_mc = [] # CapMrktCurUSD
eos_addrs = [] # AdrActCnt
eos_sply = [] # SplyCur
eos_tx = [] # TxCnt
eos_tf_tx = [] # TxTfrCnt
eos_adj_tf = []

for line in eos_reader.readlines()[1:]:
    vals = line.split(',')
    eos_mc.append(float(vals[2]))
    eos_addrs.append(int(vals[1]))
    eos_sply.append(float(vals[11]))
    eos_tx.append(int(vals[12]))
    eos_tf_tx.append(int(vals[13]))
    eos_adj_tf.append(float(vals[15]))

total_mc = [eth_mc[i] + eos_mc[i] for i in range(len(eth_mc))]
total_addrs = [eth_addrs[i] + eos_addrs[i] for i in range(len(eth_addrs))]
total_supply = [eth_sply[i] + eos_sply[i] for i in range(len(eth_sply))]
total_tx = [eth_tx[i] + eos_tx[i] for i in range(len(eth_tx))]
total_tf_tx = [eth_tf_tx[i] + eos_tf_tx[i] for i in range(len(eth_tf_tx))]
total_adj = [eth_adj_tf[i] + eos_adj_tf[i] for i in range(len(eth_adj_tf))]

with open("results2.csv", "w") as csvfile:
    fieldnames = ['total_mc', 'eth_mc', 'total_addrs', 'eth_addrs', 'eos_addrs', 'total_supply', 'eos_sply', 'price', 'total_tx', 'eth_tx', 'eos_tx', 'total_tf_tx', 'eth_tf_tx', 'eos_tf_tx', 'total_adj_tf']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(len(total_mc)):
        writer.writerow({'total_mc': str(total_mc[i]).replace('.', ','), 'eth_mc': str(eth_mc[i]).replace('.', ','), 'total_addrs': total_addrs[i], 'eth_addrs': eth_addrs[i], 'eos_addrs': eos_addrs[i], 'total_supply': str(total_supply[i]).replace('.', ','), 'eos_sply': str(eos_sply[i]).replace('.', ','), 'price': str(eth_price[i]).replace('.', ','), 'total_tx': total_tx[i], 'eth_tx': eth_tx[i], 'eos_tx':eos_tx[i], 'total_tf_tx': total_tf_tx[i], 'eth_tf_tx': eth_tf_tx[i], 'eos_tf_tx': eos_tf_tx[i], 'total_adj_tf': str(total_adj[i]).replace('.', ',')})