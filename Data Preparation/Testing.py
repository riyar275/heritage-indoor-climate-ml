import pandas as pd

file_paths = [
    r"E:\AI4ED\Dissertation\AIThermalDigitalTwin\Sam DigitalTwin\oct_jan_anonymised.xlsx",
    r"E:\AI4ED\Dissertation\AIThermalDigitalTwin\Sam DigitalTwin\jan_march_anonymised.xlsx",
    r"E:\AI4ED\Dissertation\AIThermalDigitalTwin\Sam DigitalTwin\march_may_anonymised.xlsx",
    r"E:\AI4ED\Dissertation\AIThermalDigitalTwin\Sam DigitalTwin\may_july_anonymised.xlsx"
]

outdoor_keywords = ['outside', 'external']
outdoor_dfs = []

for file in file_paths:
    xls = pd.ExcelFile(file)
    for sheet_name in xls.sheet_names:
        sheet_lower = sheet_name.lower()
        if any(keyword in sheet_lower for keyword in outdoor_keywords):
            df = xls.parse(sheet_name)

            if not {'Day Time', 'Temperature (°C)', 'Humidity (%RH)'}.issubset(df.columns):
                continue

            df = df[['Day Time', 'Temperature (°C)', 'Humidity (%RH)']].copy()
            df.columns = ['datetime', 'temperature', 'humidity']
            df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
            df = df.dropna()

            outdoor_dfs.append(df)

# Combine all outdoor sheets
merged = outdoor_dfs[0].set_index('datetime')
for df in outdoor_dfs[1:]:
    df = df.set_index('datetime')
    merged = merged.join(df, how='outer', lsuffix='', rsuffix='_other')

# Calculate mean across all temperature and humidity columns
temp_cols = [col for col in merged.columns if 'temperature' in col]
humid_cols = [col for col in merged.columns if 'humidity' in col]

merged['Outdoor_Temp'] = merged[temp_cols].mean(axis=1)
merged['Outdoor_Humidity'] = merged[humid_cols].mean(axis=1)

# Print with datetime as a column by resetting index
print(merged.reset_index()[['datetime', 'Outdoor_Temp', 'Outdoor_Humidity']].head(20))

# Resample to hourly means
hourly_outdoor = merged[['Outdoor_Temp', 'Outdoor_Humidity']].resample('h').mean().reset_index()
hourly_outdoor['datetime'] = hourly_outdoor['datetime'].dt.strftime('%d-%m-%Y %H:%M')

# Save to CSV
hourly_outdoor.to_csv("hourly_outdoor_only.csv", index=False)

print("✅ Final hourly outdoor data saved.")
print(hourly_outdoor.head())
