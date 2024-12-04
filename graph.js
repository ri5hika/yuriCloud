window.onload = function () {
    // Define the data from your Python script
    var timestamps = [
        "2024-01-01 00:00", "2024-01-01 00:01", "2024-01-01 00:02", "2024-01-01 00:03", // Add more timestamps here
        "2024-01-01 00:04", "2024-01-01 00:05", "2024-01-01 00:06", "2024-01-01 00:07"
    ];
    
    // Example data from your Python code
    var cpuUsage = [50, 52, 54, 53, 55, 89, 60, 62]; // Replace with real data
    var memoryUsage = [30, 32, 31, 29, 30, 7, 32, 33]; // Replace with real data
    var networkTraffic = [200, 210, 220, 215, 225, 400, 230, 240]; // Replace with real data

    // Anomaly detection - manually marking anomalies based on your Python logic
    var cpuAnomalies = [0, 0, 0, 0, 0, 1, 0, 0]; // Anomaly in CPU at index 5
    var memoryAnomalies = [0, 0, 0, 0, 0, 1, 0, 0]; // Anomaly in memory at index 5
    var networkAnomalies = [0, 0, 0, 0, 0, 1, 0, 0]; // Anomaly in network traffic at index 5

    // CPU Usage Graph with anomalies
    var cpuData = {
        x: timestamps,
        y: cpuUsage,
        type: 'scatter',
        mode: 'lines+markers',
        marker: { color: 'blue' }
    };

    var cpuAnomalyData = {
        x: timestamps.filter((_, i) => cpuAnomalies[i] === 1),
        y: cpuUsage.filter((_, i) => cpuAnomalies[i] === 1),
        type: 'scatter',
        mode: 'markers',
        marker: { color: 'red', size: 12 },
        name: 'CPU Anomalies'
    };

    var cpuLayout = {
        title: 'CPU Usage',
        xaxis: { title: 'Time' },
        yaxis: { title: 'CPU Usage (%)' },
        showlegend: true,
        hovermode: 'closest'
    };

    // Plot the CPU usage graph
    Plotly.newPlot('cpu-usage-chart', [cpuData, cpuAnomalyData], cpuLayout);

    // Memory Usage Graph with anomalies
    var memoryData = {
        x: timestamps,
        y: memoryUsage,
        type: 'scatter',
        mode: 'lines+markers',
        marker: { color: 'green' }
    };

    var memoryAnomalyData = {
        x: timestamps.filter((_, i) => memoryAnomalies[i] === 1),
        y: memoryUsage.filter((_, i) => memoryAnomalies[i] === 1),
        type: 'scatter',
        mode: 'markers',
        marker: { color: 'red', size: 12 },
        name: 'Memory Anomalies'
    };

    var memoryLayout = {
        title: 'Memory Usage',
        xaxis: { title: 'Time' },
        yaxis: { title: 'Memory Usage (%)' },
        showlegend: true,
        hovermode: 'closest'
    };

    // Plot the Memory usage graph
    Plotly.newPlot('memory-usage-chart', [memoryData, memoryAnomalyData], memoryLayout);

    // Network Traffic Graph with anomalies
    var networkData = {
        x: timestamps,
        y: networkTraffic,
        type: 'scatter',
        mode: 'lines+markers',
        marker: { color: 'purple' }
    };

    var networkAnomalyData = {
        x: timestamps.filter((_, i) => networkAnomalies[i] === 1),
        y: networkTraffic.filter((_, i) => networkAnomalies[i] === 1),
        type: 'scatter',
        mode: 'markers',
        marker: { color: 'red', size: 12 },
        name: 'Network Anomalies'
    };

    var networkLayout = {
        title: 'Network Traffic',
        xaxis: { title: 'Time' },
        yaxis: { title: 'Network Traffic (KBps)' },
        showlegend: true,
        hovermode: 'closest'
    };

    // Plot the Network Traffic graph
    Plotly.newPlot('network-traffic-chart', [networkData, networkAnomalyData], networkLayout);

    // Correlation Heatmap (if needed, keep the correlation logic as before)
    var correlationData = [
        {
            z: [
                [1, 0.8, 0.4],
                [0.8, 1, 0.5],
                [0.4, 0.5, 1]
            ],
            x: ['CPU Usage', 'Memory Usage', 'Network Traffic'],
            y: ['CPU Usage', 'Memory Usage', 'Network Traffic'],
            colorscale: 'Viridis',
            type: 'heatmap',
        }
    ];

    var correlationLayout = {
        title: 'Correlation Heatmap Between Metrics',
        xaxis: { title: 'Metrics' },
        yaxis: { title: 'Metrics' },
    };

    Plotly.newPlot('correlation-heatmap-chart', correlationData, correlationLayout);

    // Metric Distribution Graph
    var distributionData = [
        {
            x: Array.from({ length: 1000 }, () => Math.random() * 100),
            type: 'histogram',
            name: 'CPU Usage',
            marker: { color: 'blue' }
        },
        {
            x: Array.from({ length: 1000 }, () => Math.random() * 100),
            type: 'histogram',
            name: 'Memory Usage',
            marker: { color: 'green' }
        },
        {
            x: Array.from({ length: 1000 }, () => Math.random() * 500),
            type: 'histogram',
            name: 'Network Traffic',
            marker: { color: 'purple' }
        }
    ];

    var distributionLayout = {
        title: 'Metric Distribution (CPU, Memory, Network)',
        barmode: 'overlay',
        xaxis: { title: 'Values' },
        yaxis: { title: 'Frequency' },
    };

    Plotly.newPlot('distribution-chart', distributionData, distributionLayout);
};


