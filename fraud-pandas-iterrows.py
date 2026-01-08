import pandas as pd

# Load AND SET INDEX on accounts dataframe
accounts_df = pd.read_csv("accounts.csv").set_index("Account ID")
transactions_df = pd.read_csv("transactions.csv")
non_fraud_rows = []

for _, tx in transactions_df.iterrows():
    source_status = accounts_df.loc[tx["Source"], "Review Status"]
    dest_status = accounts_df.loc[tx["Destination"], "Review Status"]
    
    if source_status != "FRAUDULENT" and dest_status != "FRAUDULENT":
        non_fraud_rows.append(tx)

non_fraud_df = pd.DataFrame(non_fraud_rows)
print(non_fraud_df)
print(f"Number of non-fraudulent transactions: {len(non_fraud_df)}")
non_fraud_df.to_csv('output.csv', index=False)
