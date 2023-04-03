import pandas as pd
import numpy
from dotenv import load_dotenv
import os

load_dotenv()

# Reading JSON file
data = pd.read_json(os.environ.get('bitcoin_block_750000'))

# Transactions data
txs =pd.json_normalize(data['result']['tx']) 
#print(txs.columns)

# Number of transactions
#no_txs = data['result']['nTx']
no_txs = txs['txid'].count() #2496

## Task 2: Number of transactions with 1-5 outputs, 6-25 outputs, 26-100 outputs, 101+ outputs
# Lists to store transactions
txs_outputs1_5 = []
txs_outputs6_25 = []
txs_outputs26_100 = []
txs_outputs101plus = []

# Store fees of batched transactions
batched_txs_fees = []

# Loop through transactions to count outputs
for x in range(no_txs):
    # Outputs in the transaction
    tx_outputs = pd.json_normalize(data['result']['tx'][x]['vout'])
    
    # Number of outputs in the transaction
    no_outputs_tx = len(tx_outputs)    

    # Transaction
    tx = pd.json_normalize(data['result']['tx'][x])

    # Outputs 1-5
    if no_outputs_tx >= 1 and no_outputs_tx <= 5:
        txs_outputs1_5.append(tx)
    
    # Outputs 6-25
    elif no_outputs_tx >= 6 and no_outputs_tx <= 25:
        txs_outputs6_25.append(tx)

    # Outputs 26-100
    elif no_outputs_tx >= 26 and no_outputs_tx <= 100:
        txs_outputs26_100.append(tx)
        
    # Outputs equal to or greater than 101
    elif no_outputs_tx >= 101:
        txs_outputs101plus.append(tx)

        # Store fees
        batched_txs_fees.append(data['result']['tx'][x]['fee'])


no_txs_outputs1_5 = len(txs_outputs1_5)
print(f"Number of transactions with 1-5 outputs: {no_txs_outputs1_5}")

no_txs_outputs6_25 = len(txs_outputs6_25)
print(f"Number of transactions with 6-25 outputs: {no_txs_outputs6_25}")

no_txs_outputs26_100 = len(txs_outputs26_100)
print(f"Number of transactions with 26-100 outputs: {no_txs_outputs26_100}")

no_txs_outputs101plus = len(txs_outputs101plus)
print(f"Number of transactions with 101 or more outputs: {no_txs_outputs101plus}")

## Task 3: Median and average fees of batched transactions
# Average fee of batched transactions
avg_fee = '{:.8f}'.format(numpy.average(batched_txs_fees))
print(f"Average fee of batched transactions: {avg_fee}")

# Median fee of batched transactions
med_fee = '{:.8f}'.format(numpy.median(batched_txs_fees))
print(f"Median fee of batched transactions: {med_fee}")


## Task 4: Identify the most expensive transaction
# To store the most expensive transaction
most_exp_tx = []
# To store inputs of the most expensive transaction
most_exp_tx_inputs = []
# Loop through transactions to count inputs
for a in range(no_txs):
    try:    
        input_values = []
        for b in range(len(pd.json_normalize(data['result']['tx'][a]['vin']))):
            val = data['result']['tx'][a]['vin'][b]['prevout']['value']
            input_values.append(val)
        
        if sum(input_values) > sum(most_exp_tx_inputs):
            most_exp_tx = data['result']['tx'][a]
            most_exp_tx_inputs = input_values
    
    # If there is no prevout
    except KeyError:
        pass

# Txid of the most expensive transaction
most_exp_tx_txid = most_exp_tx['txid']
print(f"Txid of the most expensive transaction: {most_exp_tx_txid}")

# Number of inputs and outputs of the most expensive transaction
no_most_exp_tx_inputs = len(most_exp_tx['vin'])
print(f"Number of inputs in the most expensive transaction: {no_most_exp_tx_inputs}")

no_most_exp_tx_outputs = len(most_exp_tx['vout'])
print(f"Number of outputs in the most expensive transaction: {no_most_exp_tx_outputs}")


# Sum of inputs and outputs in the most expensive transaction
sum_most_exp_tx_inputs = sum(most_exp_tx_inputs)
print(f"Sum of inputs in the most expensive transaction: {sum_most_exp_tx_inputs}")

most_exp_tx_outputs = []
for d in range(len(most_exp_tx['vout'])):
    most_exp_tx_outputs.append(most_exp_tx['vout'][d]['value'])

sum_most_exp_tx_outputs = sum(most_exp_tx_outputs)
print(f"Sum of outputs in the most expensive transaction: {sum_most_exp_tx_outputs}")

# Difference between sum of inputs and outputs should be the transaction fee
diff = round(sum_most_exp_tx_inputs - sum_most_exp_tx_outputs, 8)
print(f"Transaction fee of the most expensive transaction: {'{:.8f}'.format(diff)}")
#print('{:.8f}'.format(most_exp_tx['fee'])) #0.00002023