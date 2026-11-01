import pandas as pd
import matplotlib.pyplot as plt

# Load your data
df = pd.read_csv(r"E:\AI4ED\Dissertation\CSV Files\Gatwick\Check.csv", parse_dates=["Datetime"])
print(df.columns)

# Parse datetime properly (dayfirst=True)
df['Datetime'] = pd.to_datetime(df['Datetime'], dayfirst=True)

# Columns of interest
columns = ['Outdoor_Temp', 'Indoor (0.01mm wall)', 'Indoor (0.1m wall)', 'Indoor (1.5m wall)', 'Indoor (2m wall)']

# Smooth the temperature data using a 24-hour rolling average
df[columns] = df[columns].rolling(window=24).mean()

# Drop NaN values created by rolling average
df = df.dropna(subset=columns)

# Extract month for filtering seasons
df['Month'] = df['Datetime'].dt.month

# Filter by winter (Dec, Jan, Feb) and summer (Jun, Jul, Aug)
df_winter = df[df['Month'].isin([12, 1, 2])]
df_summer = df[df['Month'].isin([6, 7, 8])]

# 1. Correlation check between outdoor temp and indoor temps
print("Correlation with Outdoor Temp:")
for col in columns[1:]:  # skip 'Outdoor_Temp'
    corr = df['Outdoor_Temp'].corr(df[col])
    print(f"{col}: {corr:.3f}")

# 2. Mean temperature differences (Indoor - Outdoor) for Winter and Summer
print("\nAverage Temp Differences (Indoor - Outdoor):")
for col in columns[1:]:
    diff_winter = (df_winter[col] - df_winter['Outdoor_Temp']).mean()
    diff_summer = (df_summer[col] - df_summer['Outdoor_Temp']).mean()
    print(f"{col} — Winter Diff: {diff_winter:.2f} °C, Summer Diff: {diff_summer:.2f} °C")

# 2b. Mean ± Std Dev Temp Differences
print("\nMean ± Std Dev Temp Differences (Indoor - Outdoor):")
for col in columns[1:]:
    diff_winter = df_winter[col] - df_winter['Outdoor_Temp']
    diff_summer = df_summer[col] - df_summer['Outdoor_Temp']
    print(f"{col} — Winter: {diff_winter.mean():.2f} ± {diff_winter.std():.2f} °C, "
          f"Summer: {diff_summer.mean():.2f} ± {diff_summer.std():.2f} °C")

# 3. Plot Indoor and Outdoor temperatures over time
plt.figure(figsize=(12, 6))
plt.plot(df['Datetime'], df['Outdoor_Temp'], label="Outdoor Temp", color="black", linewidth=2)

colors = ['red', 'orange', 'green', 'blue']
for i, col in enumerate(columns[1:]):
    plt.plot(df['Datetime'], df[col], label=col, alpha=0.7, color=colors[i])

plt.legend()
plt.title("Effect of Wall Thickness on Indoor Temperature vs Outdoor Temperature (2025)")
plt.ylabel("Temperature (°C)")
plt.xlabel("Date")
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
