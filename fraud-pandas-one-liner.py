import pandas as pd

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
