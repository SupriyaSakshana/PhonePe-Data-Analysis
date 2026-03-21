import os
import json
import pandas as pd

# =====================================================
# 🔷 SAFE JSON LOADER
# =====================================================
def load_json(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return None


# =====================================================
# 🔷 AGGREGATED DATA
# =====================================================
def extract_aggregated_state(base_path, data_type):
    data_list = []

    for state in os.listdir(base_path):
        state_path = os.path.join(base_path, state)
        if not os.path.isdir(state_path):
            continue

        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)

            for file in os.listdir(year_path):
                if not file.endswith('.json'):
                    continue

                file_path = os.path.join(year_path, file)
                data = load_json(file_path)

                if not data or 'data' not in data:
                    continue

                quarter = file.replace('.json', '')

                try:
                    # -------------------------------
                    # TRANSACTION / INSURANCE
                    # -------------------------------
                    if data_type in ["transaction", "insurance"]:
                        txn_data = data['data'].get('transactionData')

                        if not txn_data:
                            continue

                        for item in txn_data:
                            instruments = item.get('paymentInstruments', [])

                            for ins in instruments:
                                data_list.append({
                                    'State': state,
                                    'Year': year,
                                    'Quarter': quarter,
                                    'Type': item.get('name'),
                                    'Count': ins.get('count', 0),
                                    'Amount': ins.get('amount', 0)
                                })

                    # -------------------------------
                    # USER
                    # -------------------------------
                    elif data_type == "user":
                        users = data['data'].get('usersByDevice')

                        if not users:
                            continue

                        for item in users:
                            data_list.append({
                                'State': state,
                                'Year': year,
                                'Quarter': quarter,
                                'Brand': item.get('brand'),
                                'Count': item.get('count', 0),
                                'Percentage': item.get('percentage', 0)
                            })

                except Exception as e:
                    print(f"⚠️ Skipped {file_path}: {e}")

    return pd.DataFrame(data_list)


# =====================================================
# 🔷 MAP DATA
# =====================================================
def extract_map_state(base_path, data_type):
    data_list = []

    for state in os.listdir(base_path):
        state_path = os.path.join(base_path, state)

        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)

            for file in os.listdir(year_path):
                if not file.endswith('.json'):
                    continue

                file_path = os.path.join(year_path, file)
                data = load_json(file_path)

                if not data or 'data' not in data:
                    continue

                quarter = file.replace('.json', '')

                try:
                    if data_type in ["transaction", "insurance"]:
                        hover = data['data'].get('hoverDataList')

                        if not hover:
                            continue

                        for item in hover:
                            metric = item.get('metric', [{}])[0]

                            data_list.append({
                                'State': state,
                                'Year': year,
                                'Quarter': quarter,
                                'District': item.get('name'),
                                'Count': metric.get('count', 0),
                                'Amount': metric.get('amount', 0)
                            })

                    elif data_type == "user":
                        hover = data['data'].get('hoverData')

                        if not hover:
                            continue

                        for district, val in hover.items():
                            data_list.append({
                                'State': state,
                                'Year': year,
                                'Quarter': quarter,
                                'District': district,
                                'RegisteredUsers': val.get('registeredUsers', 0),
                                'AppOpens': val.get('appOpens', 0)
                            })

                except Exception as e:
                    print(f"⚠️ Skipped {file_path}: {e}")

    return pd.DataFrame(data_list)


# =====================================================
# 🔷 TOP DATA
# =====================================================
def extract_top_state(base_path, data_type):
    data_list = []

    for state in os.listdir(base_path):
        state_path = os.path.join(base_path, state)

        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)

            for file in os.listdir(year_path):
                if not file.endswith('.json'):
                    continue

                file_path = os.path.join(year_path, file)
                data = load_json(file_path)

                if not data or 'data' not in data:
                    continue

                quarter = file.replace('.json', '')

                try:
                    districts = data['data'].get('districts')

                    if not districts:
                        continue

                    for item in districts:
                        if data_type in ["transaction", "insurance"]:
                            metric = item.get('metric', {})

                            data_list.append({
                                'State': state,
                                'Year': year,
                                'Quarter': quarter,
                                'District': item.get('entityName'),
                                'Count': metric.get('count', 0),
                                'Amount': metric.get('amount', 0)
                            })

                        elif data_type == "user":
                            data_list.append({
                                'State': state,
                                'Year': year,
                                'Quarter': quarter,
                                'District': item.get('name'),
                                'RegisteredUsers': item.get('registeredUsers', 0)
                            })

                except Exception as e:
                    print(f"⚠️ Skipped {file_path}: {e}")

    return pd.DataFrame(data_list)


# =====================================================
# 🔷 PATHS
# =====================================================
base = r'G:\Supriya\pulse\data'
output = r'G:\Supriya\PhonePe'

os.makedirs(output, exist_ok=True)


# =====================================================
# 🔷 RUN EXTRACTION
# =====================================================
agg_tr = extract_aggregated_state(os.path.join(base, 'aggregated/transaction/country/india/state'), "transaction")
agg_us = extract_aggregated_state(os.path.join(base, 'aggregated/user/country/india/state'), "user")
agg_in = extract_aggregated_state(os.path.join(base, 'aggregated/insurance/country/india/state'), "insurance")

map_tr = extract_map_state(os.path.join(base, 'map/transaction/hover/country/india/state'), "transaction")
map_us = extract_map_state(os.path.join(base, 'map/user/hover/country/india/state'), "user")
map_in = extract_map_state(os.path.join(base, 'map/insurance/hover/country/india/state'), "insurance")

top_tr = extract_top_state(os.path.join(base, 'top/transaction/country/india/state'), "transaction")
top_us = extract_top_state(os.path.join(base, 'top/user/country/india/state'), "user")
top_in = extract_top_state(os.path.join(base, 'top/insurance/country/india/state'), "insurance")


# =====================================================
# 🔷 SAVE FILES
# =====================================================
agg_tr.to_csv(os.path.join(output, 'agg_transaction.csv'), index=False)
agg_us.to_csv(os.path.join(output, 'agg_user.csv'), index=False)
agg_in.to_csv(os.path.join(output, 'agg_insurance.csv'), index=False)

map_tr.to_csv(os.path.join(output, 'map_transaction.csv'), index=False)
map_us.to_csv(os.path.join(output, 'map_user.csv'), index=False)
map_in.to_csv(os.path.join(output, 'map_insurance.csv'), index=False)

top_tr.to_csv(os.path.join(output, 'top_transaction.csv'), index=False)
top_us.to_csv(os.path.join(output, 'top_user.csv'), index=False)
top_in.to_csv(os.path.join(output, 'top_insurance.csv'), index=False)

print("✅ ALL CSV FILES CREATED SUCCESSFULLY")