import pandas as pd

# File paths — adjust if needed
outdoor_temp_fp = r"E:\AI4ED\Dissertation\CSV Files\Norway\Outdoortemp.csv"
indoor_temp_fp = r"E:\AI4ED\Dissertation\CSV Files\Norway\Norway_03\IndoorTemp.csv"
outdoor_hum_fp = r"E:\AI4ED\Dissertation\CSV Files\Norway\Outdoorhumidity.csv"
indoor_hum_fp = r"E:\AI4ED\Dissertation\CSV Files\Norway\Norway_03\Indoorhumidity.csv"


def load_clean_csv(filepath, value_column_name):
    df = pd.read_csv(filepath, skiprows=4, header=None, names=['Datetime', value_column_name])

    # Drop metadata or bad rows
    df = df[df['Datetime'].str.match(r'\d{2}-\d{2}-\d{4} \d{2}:\d{2}|^\d{2} \w{3} \d{2}:\d{2}$', na=False)]

    print(f"\nPreview from {value_column_name}:")
    print(df.head())

    # Parse datetime
    if df['Datetime'].str.contains('-').all():
        df['Datetime'] = pd.to_datetime(df['Datetime'], format="%d-%m-%Y %H:%M", errors='raise')
    else:
        df['Datetime'] = pd.to_datetime("2025 " + df['Datetime'], format="%Y %d %b %H:%M", errors='raise')

    df[value_column_name] = pd.to_numeric(df[value_column_name], errors='coerce')
    df = df.dropna()

    return df


# Load each dataset
df_outdoor_temp = load_clean_csv(outdoor_temp_fp, 'Outdoor_Temp')
df_indoor_temp = load_clean_csv(indoor_temp_fp, 'Indoor_Temp')
df_outdoor_hum = load_clean_csv(outdoor_hum_fp, 'Outdoor_Humidity')
df_indoor_hum = load_clean_csv(indoor_hum_fp, 'Indoor_Humidity')

# Merge all data on Datetime
df = df_outdoor_temp.merge(df_indoor_temp, on='Datetime', how='inner')
df = df.merge(df_outdoor_hum, on='Datetime', how='inner')
df = df.merge(df_indoor_hum, on='Datetime', how='inner')

# Sort and clean
df = df.sort_values('Datetime')
df_clean = df.dropna()

# Save cleaned merged CSV
output_path = r"E:\AI4ED\Dissertation\CSV Files\Norway\Norway_03\Norway03.csv"
df_clean.to_csv(output_path, index=False)

print("✅ Combined and cleaned data saved to:")
print(output_path)
print(df_clean.head())