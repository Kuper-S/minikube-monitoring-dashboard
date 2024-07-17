# Minikube Monitoring Dashboard Application


## Overview

A web-based dashboard for monitoring a Minikube cluster, built with Flask, psutil, and the Kubernetes Python client.

## Features

- Real-time monitoring of CPU, memory, disk usage, and network stats.
- Pod-level metrics for CPU and memory usage.
- Responsive design for mobile and desktop views.
- Real-time chart updates with Chart.js.
- User authentication (optional).
- Deployment instructions for local and Kubernetes environments.



## Getting Started

### Prerequisites

- Docker
- Minikube
- Python 3.8+

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/minikube-monitoring-dashboard.git
    cd minikube-monitoring-dashboard
    ```

2. Build the Docker image:
    ```bash
    docker build -t minikube-monitoring .
    ```

3. Run the Docker container:
    ```bash
    docker run -p 5000:5000 minikube-monitoring
    ```

4. Access the dashboard at `http://localhost:5000`.

### Usage

- **Monitor Cluster**: View real-time metrics for CPU, memory, disk usage, and network stats.
- **Pod Metrics**: See CPU and memory usage for each pod in the cluster.

### Configuration

- Edit the `config.py` file to customize the application settings.

### Deployment

#### Local Deployment

1. Start Minikube:
    ```bash
    minikube start
    ```

2. Update kubeconfig:
    ```bash
    minikube update-context
    ```

3. Run the application:
    ```bash
    python app.py
    ```

#### Kubernetes Deployment

1. Build and push the Docker image to a container registry.
2. Deploy using Kubernetes manifests or Helm charts (included in the `k8s` directory).

### Contributing

Contributions are welcome! Please submit a pull request or open an issue for any changes or improvements.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
