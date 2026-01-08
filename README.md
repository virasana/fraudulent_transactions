# FRAUDULENT ACCOUNTS

## Overview

This repo demonstrates two different approaches to producing a list of transactions that do NOT reference fraudulent accounts in accounts.csv.

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

## Comparison

The iterrows solution is more readable and concise. 

However, the merge approach is considered marginally better as it uses vectorised operations under the hood and may perform better on very large datasets. 

Arguably, the iterrows solution is better in this case, as for very large datasets we might look to other means of querying the data (such as a dedicated database service).

## In Sum

* iterrows: concise!
* merge: theoretically preferred



