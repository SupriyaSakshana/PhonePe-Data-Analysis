import os
import json
import pandas as pd

path = r'G:\Supriya\pulse\data\aggregated\transaction\country\india'

data_list = []

for year in os.listdir(path):
    year_path = os.path.join(path, year)
    
    for file in os.listdir(year_path):
        if file.endswith('.json'):
            file_path = os.path.join(year_path, file)
            
            with open(file_path, 'r') as f:
                data = json.load(f)
                
                try:
                    for item in data['data']['transactionData']:
                        name = item['name']
                        
                        for ins in item['paymentInstruments']:
                            count = ins['count']
                            amount = ins['amount']
                            
                            data_list.append({
                                'Year': year,
                                'Quarter': file.replace('.json', ''),
                                'Type': name,
                                'Count': count,
                                'Amount': amount
                            })
                except:
                    pass

df = pd.DataFrame(data_list)

print(df.head())



df.to_csv('transaction_data.csv', index=False)




