import matplotlib
matplotlib.use('Agg')

from flask import Flask, render_template, send_from_directory
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import csv
import io

# Initialize Flask app
app = Flask(__name__)

# Set Seaborn style for better visuals
sns.set(style="whitegrid")

# Define the path to the static/images directory
images_dir = "static/images"

# Create the static images folder if it doesn't exist
if not os.path.exists(images_dir):
    os.makedirs(images_dir)

# Data Preparation (Your anomaly detection logic)
def prepare_data():
    np.random.seed(42)
    n_samples = 1000

    # Simulate data (CPU, Memory, Network Traffic)
    cpu_usage = np.random.normal(50, 5, n_samples)
    cpu_usage[980:] = np.random.normal(80, 3, 20)  # Anomaly

    memory_usage = np.random.normal(30, 8, n_samples)
    memory_usage[950:] = np.random.normal(70, 5, 50)  # Anomaly

    network_traffic = np.random.normal(200, 20, n_samples)
    network_traffic[100:120] = np.random.normal(400, 25, 20)  # Anomaly

    # Create DataFrame
    df = pd.DataFrame({
        'timestamp': pd.date_range(start='2024-01-01', periods=n_samples, freq='min'),
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
        'network_traffic': network_traffic
    })

    return df

# Function to detect anomalies (Z-Score)
def detect_anomalies(df):
    def z_score_anomaly(metric_data):
        mean = metric_data.mean()
        std = metric_data.std()
        z_scores = (metric_data - mean) / std
        return z_scores.apply(lambda x: 1 if abs(x) > 3 else 0)

    df['cpu_anomaly'] = z_score_anomaly(df['cpu_usage'])
    df['memory_anomaly'] = z_score_anomaly(df['memory_usage'])
    df['network_anomaly'] = z_score_anomaly(df['network_traffic'])
    return df

# Function to generate and save plots
def generate_plots(df):
    # CPU Usage with Anomalies
    plt.figure(figsize=(14, 5))
    plt.plot(df['timestamp'], df['cpu_usage'], label='CPU Usage', color='blue')
    plt.scatter(df[df['cpu_anomaly'] == 1]['timestamp'], df[df['cpu_anomaly'] == 1]['cpu_usage'], color='red', label='CPU Anomaly')
    plt.legend()
    plt.title('CPU Usage and Anomalies')
    plt.xlabel('Timestamp')
    plt.ylabel('CPU Usage (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "cpu_usage.png"))
    plt.close()

    # Memory Usage with Anomalies
    plt.figure(figsize=(14, 5))
    plt.plot(df['timestamp'], df['memory_usage'], label='Memory Usage', color='green')
    plt.scatter(df[df['memory_anomaly'] == 1]['timestamp'], df[df['memory_anomaly'] == 1]['memory_usage'], color='red', label='Memory Anomaly')
    plt.legend()
    plt.title('Memory Usage and Anomalies')
    plt.xlabel('Timestamp')
    plt.ylabel('Memory Usage (MB)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "memory_usage.png"))
    plt.close()

    # Network Traffic with Anomalies
    plt.figure(figsize=(14, 5))
    plt.plot(df['timestamp'], df['network_traffic'], label='Network Traffic', color='purple')
    plt.scatter(df[df['network_anomaly'] == 1]['timestamp'], df[df['network_anomaly'] == 1]['network_traffic'], color='red', label='Network Anomaly')
    plt.legend()
    plt.title('Network Traffic and Anomalies')
    plt.xlabel('Timestamp')
    plt.ylabel('Network Traffic (KBps)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(images_dir, "network_traffic.png"))
    plt.close()

# Email Alert Functionality
def send_email_alert(subject, body, recipient_email):
    sender_email = "yuvika.hay@gmail.com"
    sender_password = "kjfi dtro tlda vrcm"

    # Set up the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print(f"Alert sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Email with CSV Attachment
def send_email_with_csv(subject, body, recipient_email, csv_path):
    sender_email = "yuvika.hay@gmail.com"
    sender_password = "kjfi dtro tlda vrcm"

    # Set up the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Attach the CSV file
    try:
        with open(csv_path, "rb") as file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(csv_path)}')
        msg.attach(part)

        # Send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print(f"Alert with CSV sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email with CSV: {e}")

# Check and alert anomalies
def check_and_alert_anomalies(df, recipient_email):
    anomalies = pd.DataFrame()
    for metric in ['cpu_usage', 'memory_usage', 'network_traffic']:
        metric_anomalies = df[df[f"{metric.split('_')[0]}_anomaly"] == 1]
        if not metric_anomalies.empty:
            anomalies = pd.concat([anomalies, metric_anomalies], ignore_index=True)

    if not anomalies.empty:
        # Save anomalies to a CSV file
        csv_path = "static/Anomalies.csv"
        anomalies.to_csv(csv_path, index=False)

        # Send email with CSV attachment
        send_email_with_csv("Anomaly Report: Cloud Infrastructure Monitoring", "As part of our commitment to providing seamless monitoring of your cloud infrastructure, we have detected potential anomalies in the system. Please find attached the detailed anomaly report in CSV format for your review. This report highlights irregularities in key metrics, including CPU usage, memory usage, and network traffic, that may require immediate attention.", recipient_email, csv_path)

# Flask route
@app.route('/')
def dashboard():
    return render_template('login.html')


@app.route('/index')
def index():
    df = prepare_data()
    return render_template('index.html',
                           cpu_usage='static/images/cpu_usage.png', 
                           memory_usage='static/images/memory_usage.png', 
                           network_traffic='static/images/network_traffic.png')

@app.route('/ai')
def ai():
    return render_template('ai.html')

@app.route('/exp')
def exp():
    return render_template('exp.html')

@app.route('/graph')
def graph():
    df = prepare_data()
    df = detect_anomalies(df)
    generate_plots(df)
    check_and_alert_anomalies(df, "rishikasingh0005@gmail.com")
    return render_template('graph.html')

@app.route('/dash')
def login():
    return render_template('dash.html')

@app.route('/acc')
def acc():
    return render_template('acc.html')

if __name__ == '__main__':
    app.run(debug=True)
