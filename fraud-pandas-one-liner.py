import pandas as pd

# This approach uses Pandas datasets and is the most elegant code.
# This uses 'join' logic, familiar to relational datasets,
# whereby a lookup is performed on accounts.csv using a familiar SQL query pattern i.e.
# SELECT ... FROM table1 WHERE ... IN (SELECT ... from table2)

# Load CSVs
accounts_df = pd.read_csv('accounts.csv')
transactions_df = pd.read_csv('transactions.csv')

fraudulent_accounts_df = accounts_df.loc[accounts_df['Review Status'] == 'FRAUDULENT', 'Account ID']

# 'One-liner': select only transactions where Source OR Destination are fraudulent
fraud_transactions = transactions_df[
    transactions_df['Source'].isin(fraudulent_accounts_df) 
    |
    transactions_df['Destination'].isin(fraudulent_accounts_df)
]

print(fraud_transactions)
print(f"Number of fraudulent transactions: {len(fraud_transactions)}")
