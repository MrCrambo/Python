import csv
import glob

def makeResultsCsv(filename, result_filename, token):
    reader = open(filename, "r")
    date = [] # date
    mc = [] # CapMrktCurUSD
    addrs = [] # AdrActCnt
    sply = [] # SplyCur
    price = [] # PriceUSD
    tx = [] # TxCnt
    tf_tx = [] # TxTfrCnt
    adj_tf = [] # all transfer cost
    roi = []
    roi_30 = []
    vty_30d = []
    vty_180d = []


    line1 = reader.readline().split(',')
    try:
        mc_index = line1.index('CapMrktCurUSD')
    except:
        mc_index = -1

    try:
        addrs_index = line1.index('AdrActCnt')
    except:
        addrs_index = -1

    try:
        sply_index = line1.index('SplyCur')
    except:
        sply_index = -1

    try:
        price_index = line1.index('PriceUSD')
    except:
        price_index = -1

    try:
        tx_index = line1.index('TxCnt')
    except:
        tx_index = -1

    try:
        tf_tx_index = line1.index('TxTfrCnt')
    except:
        tf_tx_index = -1

    try:
        adj_tf_index = line1.index('TxTfrValUSD')
    except:
        adj_tf_index = -1

    try:
        roi_index = line1.index('ROI1yr')
    except:
        roi_index = -1

    try:
        vty_30d_index = line1.index('VtyDayRet30d')
    except:
        vty_30d_index = -1

    try:
        roi_30_index = line1.index('ROI30d')
    except:
        roi_30_index = -1

    try:
        vty_180d_index = line1.index('VtyDayRet180d')
    except:
        vty_180d_index = -1

    for line in reader.readlines():
        vals = line.split(',')

        if vals[0] >= "2019-01-01":
            date.append(vals[0])
            if mc_index != -1:
                mc.append(vals[mc_index])
            if addrs_index != -1:
                addrs.append(vals[addrs_index])
            if sply_index != -1:
                sply.append(vals[sply_index])
            if price_index != -1:
                price.append(vals[price_index])
            if tx_index != -1:
                tx.append(vals[tx_index])
            if tf_tx_index != -1:
                tf_tx.append(vals[tf_tx_index])
            if adj_tf_index != -1:
                adj_tf.append(vals[adj_tf_index])
            if roi_index != -1:
                roi.append(vals[roi_index])
            if vty_30d_index != -1:
                vty_30d.append(vals[vty_30d_index])
            if roi_30_index != -1:
                roi_30.append(vals[roi_30_index])
            if vty_180d_index != -1:
                vty_180d.append(vals[vty_180d_index])

    with open(result_filename, "w") as csvfile:
        fieldnames = [token + '_date', token + '_total_mc', token + '_total_addrs', token + '_total_supply', token + '_price', token + '_total_tx', token + '_total_tf_tx', token + '_total_adj_tf', token + '_roi_1yr', token + '_roi_30d', token + '_vty_180d', token + '_vty_30d']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(len(mc)):
            writer.writerow({token + '_date': date[i],token + '_total_mc': str(mc[i]).replace('.', ','), token + '_total_addrs': addrs[i], token + '_total_supply': str(sply[i]).replace('.', ','), token + '_price': str(price[i]).replace('.', ','), token + '_total_tx': tx[i], token + '_total_tf_tx': tf_tx[i], token + '_total_adj_tf': str(adj_tf[i]).replace('.', ','), token + '_roi_1yr': str(roi[i]).replace('.', ','), token + '_roi_30d': str(roi_30[i]).replace('.', ','), token + '_vty_180d': str(vty_180d[i]).replace('.', ','), token + '_vty_30d': str(vty_30d[i]).replace('.', ',')})

csv_files = [f for f in glob.glob("*") if "csv" in f]

for f in csv_files:
    print(f)
    makeResultsCsv(f, 'results_' + f.split('.')[0] + '.csv', f.split('.')[0])