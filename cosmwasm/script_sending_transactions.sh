#!/bin/bash

#first you need export theses variables

echo $APPROVE
echo $CONTRACT
echo ""
echo ""


TIMEFORMAT=%R



#count max transaction for the script
MAX=5




echo "clear results file ? y/n"
read op



#clear the file content 
if [[ $op -eq "y" ]]
then

echo "" > results_transactions.txt	

fi



#interator for sendind transactions to the contract
#and saving the results on the results_transactions file
for (( i=1; i<=$MAX; i++ ))
do

echo ""
echo ""
echo "Transaction Number: $i of $MAX " >> results_transactions.txt
echo ""
{ time wasmcli tx wasm execute $CONTRACT "$APPROVE" --from doctor --chain-id="localnet" --gas-prices="0.025ucosm" --gas="auto" --gas-adjustment="1.2" -y ; } 2>> results_transactions.txt
echo "" >> results_transactions.txt

  
done







