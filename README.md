# FRAUDULENT ACCOUNTS

## Overview

This repo demonstrates a few different approaches to producing a list of transactions that reference fraudulent accounts in accounts.csv.  These variously produce either fraudulent or non-fraudulent transactions - I will standardise the code in due course!

These solutions were both produced in tandem with ChatGPT, incorporating my oversight and direction.  The key insight I provided was to implement an index to facilitate fast lookups.

## Approach 1 - Merge Rows with Pandas

File: [fraud-pandas-merge.py](./fraud-pandas-merge.py)

This approach uses pandas to load the csv data into DataFrames: accounts_df and transactions_df. 
A merge is then performed between transactions_df and accounts_df, employing a left join on Source --> Account ID. 
A similar merge is performed on this dataframe, but this time joining on  Destination --> Account ID

## Approach 2 - Iteration with Indexed Data Frame for Lookups

File: [fraud-pandas-iterrows.py](./fraud-pandas-iterrows.py)

Similar to the above, two pandas DataFrames are populated from the csv files. 
However, the index is set to  Account ID on accounts_df.  
With the index in place, we can then use df.iterrows() and .loc[index, field_name] to iterate over transactions with minimal performance overhead.  

## One-liner approach

File: [fraud-pandas-one-liner.py](./fraud-pandas-one-liner.py)

This approach utilises a pattern commonly used in SQL statements (functionally equivalent to a left join):

```sql
SELECT * FROM transactions where transactions.Source IN (SELECT AccountID from accounts WHERE AccountStatus == 'FRAUDULENT') OR transactions.Destination IN (SELECT AccountID from accounts WHERE AccountStatus == 'FRAUDULENT')
```

## Alternative approach - dictionary with simple csv iteration

This approach (not included in this repo) does not use pandas.  Rather, the idea is to load both CSVs using the standard csv reader, where accounts.csv would be transformed into a dictionary for quick lookups by key: AccountID. 

This is the simplest approach, albeit with slightly more verbose code, avoiding any requirement for the developer to understand pandas. 

However, this approach is also the slowest, as it does not take advantage of the optimisations that pandas provides.


## Comparison

The iterrows solution is simple, readable and concise, but **slowest**.

The merge approach uses vectorised operations under the hood and may perform better on very large datasets but is also **verbose** by comparison.

The one-liner is most concise, readable and performant and does this job most elegantly of all.  However, it is not as **flexible** (maintainable) - for example, we will find it difficult to output which account (Source, Destination) is fraudulent. 


My vote foes to the **one-liner** as it does the current task elegantly and performs best.








