import pandas as pd

# This approach is simple, reliable and will scale (without blowing up the memory)
# However, the iterrows reader will be slower than a Pandas Dataframe, 
# Pandas being optimised under the hood.

# Load AND SET INDEX on accounts dataframe
accounts_df = pd.read_csv("accounts.csv").set_index("Account ID")
transactions_df = pd.read_csv("transactions.csv")
fraud_rows = []

for _, tx in transactions_df.iterrows():
    source_status = accounts_df.loc[tx["Source"], "Review Status"]
    dest_status = accounts_df.loc[tx["Destination"], "Review Status"]
    
    if source_status == "FRAUDULENT" or dest_status == "FRAUDULENT":
        fraud_rows.append(tx)

fraud_df = pd.DataFrame(fraud_rows)
print(fraud_df)
print(f"Number of fraudulent transactions: {len(fraud_df)}")
# fraud_df.to_csv('output.csv', index=False)
