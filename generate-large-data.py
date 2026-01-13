import csv
import random
import os

def generate_accounts(file_name="accounts_1GB.csv", target_size_gb=1, num_accounts=200000):
    """Generate accounts CSV (~1GB) with 10% FRAUDULENT"""
    target_bytes = target_size_gb * 1024**3
    header = ["Account ID", "Account Name", "Review Status"]
    statuses = ["OK", "FRAUDULENT"]

    with open(file_name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)

        count = 1
        total_bytes = f.tell()
        while total_bytes < target_bytes:
            account_id = f"A{count:07d}"
            account_name = f"Account_{count}"
            # 10% FRAUDULENT
            status = "FRAUDULENT" if random.random() < 0.1 else "OK"
            writer.writerow([account_id, account_name, status])
            count += 1
            if count % 1000 == 0:
                total_bytes = f.tell()

    print(f"Generated {file_name}, size: {os.path.getsize(file_name)/1024**3:.2f} GB")
    return [f"A{i:07d}" for i in range(1, count)]  # return list of account IDs

def generate_transactions(file_name="transactions_1GB.csv", target_size_gb=1, account_ids=None):
    """Generate transactions CSV (~1GB) ensuring each account appears at least once"""
    if account_ids is None:
        raise ValueError("account_ids must be provided")

    target_bytes = target_size_gb * 1024**3
    header = ["Transaction ID", "Source", "Destination", "Amount"]
    num_accounts = len(account_ids)

    with open(file_name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)

        count = 1
        total_bytes = f.tell()

        # Step 1: Ensure every account appears at least once
        for acc in account_ids:
            # Random other account as destination
            dest = random.choice(account_ids)
            while dest == acc:
                dest = random.choice(account_ids)
            amount = random.randint(10, 1000)
            txn_id = f"T{count:09d}"
            writer.writerow([txn_id, acc, dest, amount])
            count += 1
            if count % 1000 == 0:
                total_bytes = f.tell()

        # Step 2: Fill remaining transactions randomly until file reaches target size
        while total_bytes < target_bytes:
            src = random.choice(account_ids)
            dest = random.choice(account_ids)
            while dest == src:
                dest = random.choice(account_ids)
            amount = random.randint(10, 1000)
            txn_id = f"T{count:09d}"
            writer.writerow([txn_id, src, dest, amount])
            count += 1
            if count % 1000 == 0:
                total_bytes = f.tell()

    print(f"Generated {file_name}, size: {os.path.getsize(file_name)/1024**3:.2f} GB")
    return count - 1  # total transactions written

if __name__ == "__main__":
    print("Generating accounts CSV...")
    accounts = generate_accounts("accounts_1GB.csv", target_size_gb=1, num_accounts=200000)

    print("Generating transactions CSV...")
    total_txns = generate_transactions("transactions_1GB.csv", target_size_gb=1, account_ids=accounts)

    print(f"Total accounts: {len(accounts)}, Total transactions: {total_txns}")
