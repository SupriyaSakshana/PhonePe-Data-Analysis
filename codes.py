import pandas as pd
import json
import os

# ================================
# PATH
# ================================
path = r'G:\Supriya\pulse\data\aggregated\insurance\country\india\state'

# ================================
# DATA STORAGE
# ================================
Ins = {
    'State': [],
    'Year': [],
    'Quarter': [],
    'Transaction_type': [],
    'Transaction_count': [],
    'Transaction_amount': []
}

# ================================
# EXTRACTION
# ================================
for state in os.listdir(path):
    state_path = os.path.join(path, state)

    if not os.path.isdir(state_path):
        continue

    for year in os.listdir(state_path):
        year_path = os.path.join(state_path, year)

        for file in os.listdir(year_path):
            if file.endswith('.json'):
                file_path = os.path.join(year_path, file)

                with open(file_path, 'r') as f:
                    data = json.load(f)

                    try:
                        for item in data['data']['transactionData']:
                            name = item['name']
                            count = item['paymentInstruments'][0]['count']
                            amount = item['paymentInstruments'][0]['amount']

                            Ins['State'].append(state)
                            Ins['Year'].append(year)
                            Ins['Quarter'].append(int(file.replace('.json', '')))
                            Ins['Transaction_type'].append(name)
                            Ins['Transaction_count'].append(count)
                            Ins['Transaction_amount'].append(amount)

                    except Exception as e:
                        print(f"Skipped {file_path}: {e}")

# ================================
# CREATE DATAFRAME
# ================================
df = pd.DataFrame(Ins)

print("Shape:", df.shape)
print(df.head())

# ================================
# SAVE CSV (FIXED LOCATION)
# ================================
output_path = r'G:\Supriya\PhonePe\aggregated_insurance_state.csv'
df.to_csv(output_path, index=False)

print(f"\n✅ CSV saved at: {output_path}")
