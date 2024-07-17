from flask import Flask, render_template
import psutil
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import logging
import datetime

app = Flask(__name__)

# Load Kubernetes configuration
try:
    config.load_kube_config()  # Use the default kubeconfig file (typically ~/.kube/config)
    contexts, active_context = config.list_kube_config_contexts()
    logging.info(f"Active Kubernetes context: {active_context['name']}")
except Exception as e:
    logging.error(f"Error loading kube config: {e}")

# Create Kubernetes API clients
v1 = client.CoreV1Api()
metrics_client = client.CustomObjectsApi()

# Sample data collection for CPU usage over time
cpu_usage_data = []
cpu_labels = []

@app.route('/')
def index():
    global cpu_usage_data, cpu_labels

    try:
        # Gathering system statistics using psutil
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        net_io = psutil.net_io_counters()
        net_sent = net_io.bytes_sent
        net_recv = net_io.bytes_recv

        # Collect CPU usage data over time for the chart
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        cpu_usage_data.append(cpu)
        cpu_labels.append(current_time)
        
        # Keep the last 10 entries to avoid overcrowding the chart
        cpu_usage_data = cpu_usage_data[-10:]
        cpu_labels = cpu_labels[-10:]

        # Gathering Kubernetes cluster statistics
        nodes = v1.list_node()
        pods = v1.list_pod_for_all_namespaces()

        pod_metrics = []
        for pod in pods.items:
            try:
                metrics = metrics_client.get_namespaced_custom_object(
                    group="metrics.k8s.io",
                    version="v1beta1",
                    namespace=pod.metadata.namespace,
                    plural="pods",
                    name=pod.metadata.name
                )
                cpu_usage = metrics['containers'][0]['usage']['cpu']
                memory_usage = metrics['containers'][0]['usage']['memory']
            except ApiException as e:
                logging.error(f"Error fetching metrics for pod {pod.metadata.name}: {e}")
                cpu_usage = 'N/A'
                memory_usage = 'N/A'

            pod_metrics.append({
                'name': pod.metadata.name,
                'namespace': pod.metadata.namespace,
                'cpu': cpu_usage,
                'memory': memory_usage
            })

        # Rendering the HTML template with the gathered statistics
        return render_template('index.html', cpu=cpu, memory=memory, disk=disk, net_sent=net_sent, net_recv=net_recv,
                               nodes=len(nodes.items), pods=len(pods.items), pod_metrics=pod_metrics,
                               cpu_usage_data=cpu_usage_data, cpu_labels=cpu_labels)

    except ApiException as e:
        logging.error(f"Kubernetes API error: {e}")
        return render_template('error.html', error_message="Kubernetes API error: An error occurred while trying to fetch data from the Kubernetes API.", error_details=str(e))

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return render_template('error.html', error_message="An unexpected error occurred while processing your request.", error_details=str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
