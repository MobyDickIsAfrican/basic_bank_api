This is an a python Djnango api that allows users to create bank accounts, deposit, transact and an
admin to view all users and transactions. 

To create a user in the terminal:
run http --json POST http://127.0.0.1:8000/api/account/user/profile email="[email]" password="[password]" 
    name="[name]" surname="[surname]" identity_number="[identity_number]" contact="[contact]"

For a user to get their account summary:
run http --json GET http://127.0.0.1:8000/api/account/user/summary/[user_primary_key]

To create a savings account:
run http --json POST http://127.0.0.1:8000/api/account/savings profile="[user_primary_key]" amount="[amount]" 

To create a credit account:
run http --json POST http://127.0.0.1:8000/api/account/credit profile="[user_primary_key]" amount="[amount]"

To make a transaction:
run http --json POST http://127.0.0.1:8000/api/account/transact from_account="[from_account]" action="[action]"
    amount="amount" type="[type]"

"from_account" is the primary key of the account making the transaction, "action" is either "W" (withdraw) or
"D" (deposit). "type" is either "savings" or "credit". 

To download the csv report of all users and accounts:
run http GET  http://127.0.0.1:8000/api/account/report > report.csv

To view all accounts and transactions by user go to: http://127.0.0.1:8000/custom-admin/[user_primary_key]





