import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set Seaborn style for better visuals
sns.set(style="whitegrid")

# 1. Data Preparation: Simulate More Complex Data
np.random.seed(42)
n_samples = 1000  # Increased data points

# Generate multiple metrics (e.g., CPU, Memory, Network Traffic)
cpu_usage = np.random.normal(50, 5, n_samples)  # Normal CPU data
cpu_usage[980:] = np.random.normal(89, 3, 20)   # CPU anomalies at the end

memory_usage = np.random.normal(30, 8, n_samples)  # Normal Memory data
memory_usage[950:] = np.random.normal(7, 5, 50)   # Memory spike anomalies

network_traffic = np.random.normal(200, 20, n_samples)  # Normal traffic
network_traffic[100:120] = np.random.normal(400, 25, 20)  # Early traffic anomaly

# Combine all data into a DataFrame
df = pd.DataFrame({
    'timestamp': pd.date_range(start='2024-01-01', periods=n_samples, freq='T'),  # Time-based data
    'cpu_usage': cpu_usage,
    'memory_usage': memory_usage,
    'network_traffic': network_traffic
})

print(df.head())

# 2. Anomaly Detection using Z-Score for Each Metric
def detect_anomalies(metric_data):
    mean = metric_data.mean()
    std = metric_data.std()
    z_scores = (metric_data - mean) / std
    return z_scores.apply(lambda x: 1 if abs(x) > 3 else 0)

# Apply anomaly detection to each metric
df['cpu_anomaly'] = detect_anomalies(df['cpu_usage'])
df['memory_anomaly'] = detect_anomalies(df['memory_usage'])
df['network_anomaly'] = detect_anomalies(df['network_traffic'])

# Print anomalies summary
print("CPU Anomalies:\n", df[df['cpu_anomaly'] == 1])
print("Memory Anomalies:\n", df[df['memory_anomaly'] == 1])
print("Network Traffic Anomalies:\n", df[df['network_anomaly'] == 1])

# 3. Visualization of Data and Anomalies

# Plot CPU Usage with Anomalies
plt.figure(figsize=(14, 5))
plt.plot(df['timestamp'], df['cpu_usage'], label='CPU Usage', color='blue')
plt.scatter(df[df['cpu_anomaly'] == 1]['timestamp'], 
            df[df['cpu_anomaly'] == 1]['cpu_usage'], 
            color='red', label='CPU Anomaly')
plt.legend()
plt.title('CPU Usage and Anomalies')
plt.xlabel('Timestamp')
plt.ylabel('CPU Usage (%)')
plt.xticks(rotation=45)
plt.show()

# Plot Memory Usage with Anomalies
plt.figure(figsize=(14, 5))
plt.plot(df['timestamp'], df['memory_usage'], label='Memory Usage', color='green')
plt.scatter(df[df['memory_anomaly'] == 1]['timestamp'], 
            df[df['memory_anomaly'] == 1]['memory_usage'], 
            color='red', label='Memory Anomaly')
plt.legend()
plt.title('Memory Usage and Anomalies')
plt.xlabel('Timestamp')
plt.ylabel('Memory Usage (MB)')
plt.xticks(rotation=45)
plt.show()

# Plot Network Traffic with Anomalies
plt.figure(figsize=(14, 5))
plt.plot(df['timestamp'], df['network_traffic'], label='Network Traffic', color='purple')
plt.scatter(df[df['network_anomaly'] == 1]['timestamp'], 
            df[df['network_anomaly'] == 1]['network_traffic'], 
            color='red', label='Network Anomaly')
plt.legend()
plt.title('Network Traffic and Anomalies')
plt.xlabel('Timestamp')
plt.ylabel('Network Traffic (KBps)')
plt.xticks(rotation=45)
plt.show()

# 4. Heatmap for Correlation Analysis
plt.figure(figsize=(8, 6))
corr = df[['cpu_usage', 'memory_usage', 'network_traffic']].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Between Metrics')
plt.show()

# 5. Distribution of Metrics
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
sns.histplot(df['cpu_usage'], ax=axes[0], kde=True, color='blue').set(title='CPU Usage Distribution')
sns.histplot(df['memory_usage'], ax=axes[1], kde=True, color='green').set(title='Memory Usage Distribution')
sns.histplot(df['network_traffic'], ax=axes[2], kde=True, color='purple').set(title='Network Traffic Distribution')
plt.show()
