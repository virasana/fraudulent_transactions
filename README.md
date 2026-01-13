# FRAUDULENT ACCOUNTS

## Overview

This repo demonstrates a few different approaches to producing a list of transactions, using two csv files (accounts.csv and transactions.csv).  The data is relational, requiring a lookup from transactions.csv into accounts.csv to determine whether the account is fraudulent. 

These solutions were both produced with the help of ChatGPT but the designs and refinements are ultimately my own.

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

## Approach 3 - One-liner approach

File: [fraud-pandas-one-liner.py](./fraud-pandas-one-liner.py)

This approach utilises a pattern commonly used in SQL statements (functionally equivalent to an inner join) and is (in my view) the most elegant:

```sql
SELECT * FROM transactions where transactions.Source IN (SELECT AccountID from accounts WHERE AccountStatus == 'FRAUDULENT') OR transactions.Destination IN (SELECT AccountID from accounts WHERE AccountStatus == 'FRAUDULENT')
```

## Approach 4 - Fraud Simple - dictionary cache with csv iteration

This approach does not use pandas.  Rather, the idea is to load the accounts into memory using the standard csv DictReader.

This approach is memory efficient and can handle a [transactions.csv](./transactions.csv) file of infinite size.  
By contrast, the [accounts.csv](./accounts.csv) file must be small enough to be able to fit into the available memory.

All of the other approaches are unable to load super-large transactions files, as they rely upon loading the entire file into memory!  This approach is therefore recommended if the transactions file is inordinately large.

## Comparison

The [iterrows](./fraud-pandas-iterrows.py) solution is simple, readable and concise, but **slowest**.

The [merge](./fraud-pandas-merge.py) approach uses vectorised operations under the hood and may perform better on very large datasets but is also **verbose** by comparison.

The [one-liner](./fraud-pandas-one-liner.py) is most concise, readable and performant and does this job most elegantly of all.  However, it is not as **flexible** (maintainable) - for example, we will find it difficult to output which account (Source, Destination) is fraudulent. 

The [simple solution](./fraud-simple.py) is able to handle an indefinitely large transaction file (**scalable**), and beats all other solutions in this regard. However, because it reads the transactions line by line, it is **slow**. All other solutions load the transactions into memory and are therefore memory-dependent, related to transactions.  Note that this approach is still constrained by the size of accounts.csv - this needs to be small enough to fit the available memory, as it is cached at the start.


My vote goes to the [one-liner](./fraud-pandas-one-liner.py) as it does the current task elegantly and performs best.  If using huge files, however, the [simple solution](./fraud-simple.py) is best.


## Profiler

As proof of the above observations, please see the output below:


| Script                    | Peak Memory (MB) | Elapsed Time (s) |
|---------------------------|----------------|----------------|
| fraud-pandas-iterrows.py  | 6480.7         | 58.58          |
| fraud-pandas-merge.py     | 6305.59        | 57.24          |
| fraud-pandas-one-liner.py | 6343.95        | 45.78          |
| **fraud-simple.py**           | **372.48**         | **567.18**         |


Voila!

As expected, [fraud-simple.py](./fraud-simple.py) consumes the least memory (by far) but is also slowest!

[fraud-pandas-one-liner.py](./fraud-pandas-one-liner.py) is marginally quicker than the other Pandas approaches but with similar memory consumption.



## Profiler Setup 

* Generate some sample data (you will need 2GB of disk space) - [generate-large-data.py](./generate-large-data.py) 

* Run the profiler yourself - [profiler.py](./profiler.py)