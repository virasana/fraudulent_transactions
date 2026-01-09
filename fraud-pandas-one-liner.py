import pandas as pd

# Load CSVs
accounts_df = pd.read_csv('accounts.csv')
transactions_df = pd.read_csv('transactions.csv')

# One-liner: select only transactions where Source OR Destination are fraudulent
fraud_transactions = transactions_df[
    transactions_df['Source'].isin(accounts_df.loc[accounts_df['Review Status'] == 'FRAUDULENT', 'Account ID']) 
    |
    transactions_df['Destination'].isin(accounts_df.loc[accounts_df['Review Status'] == 'FRAUDULENT', 'Account ID'])
]

print(fraud_transactions)
print(f"Number of fraudulent transactions: {len(fraud_transactions)}")
