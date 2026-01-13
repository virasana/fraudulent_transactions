import pandas as pd

# This approach uses Pandas data frames, with merging and is 
# hightly performant. 
# However, this approach loads the main dataset (transactions.csv) into memory
# and so will exhibit diminishing returns with larger datasets.

accounts_df = pd.read_csv("accounts.csv")
transactions_df = pd.read_csv("transactions.csv") 

merged_df = transactions_df.merge(
    accounts_df[['Account ID', 'Review Status']],
    left_on='Source',
    right_on='Account ID',
    how='left'
).rename(columns={'Review Status': 'Source Status'}).drop(columns=['Account ID'])

merged_df = merged_df.merge(
    accounts_df[['Account ID', 'Review Status']],
    left_on='Destination',
    right_on='Account ID',
    how='left'
).rename(columns={'Review Status': 'Destination Status'}).drop(columns=['Account ID'])

non_fraud_df = merged_df[
    (merged_df['Source Status'] == 'FRAUDULENT') 
    |
    (merged_df['Destination Status'] == 'FRAUDULENT')
]

print(non_fraud_df)
print(f"Number of non-fraudulent transactions: {len(non_fraud_df)}")

# non_fraud_df.to_csv('output.csv', index=False)
