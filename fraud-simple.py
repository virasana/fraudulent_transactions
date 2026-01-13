import csv

accounts = []

# cache accounts list for easy lookup --> memory hit, but probably OK 
# as number of fraud accounts is estimated to be reasonably cacheable (size-wise)
with open('accounts.csv', newline = '') as f:
    dict_reader = csv.DictReader(f)
    accounts = {account['Account ID'] 
        for account in dict_reader if account['Review Status'] == 'FRAUDULENT'
    }

# Avoid loading transactions into memory as this will be a huge hit at scale.
# Rather read line by line. 
# This will be slower than loading it into memory in one hit with a Pandas DataFrame
# But will be able to process infinitely large datasets (slowly!)
transaction_count = 0
with open('fraud.csv', 'w', newline='') as out_file, open('transactions.csv', newline = '') as f: 
        dict_reader = csv.DictReader(f)
        writer = csv.DictWriter(out_file, fieldnames=dict_reader.fieldnames)
        writer.writeheader()

        for transaction in dict_reader:
            if transaction['Source'] in accounts or transaction['Destination'] in accounts:
                writer.writerow(transaction)
                print(transaction)
                transaction_count += 1

print(transaction_count)