import time
import random
from prometheus_client import start_http_server, Counter, Gauge, Histogram, Summary

# ==============================================================================
# DEFINISIKAN METRIK TERLEBIH DAHULU (Pastikan nama variabel sesuai!)
# ==============================================================================

# 1-3: Counter Metrics
HTTP_REQUESTS = Counter('ml_api_requests_total', 'Total number of inference requests')
SUCCESS_COUNT = Counter('ml_api_success_total', 'Total number of successful predictions')
FAILURE_COUNT = Counter('ml_api_failure_total', 'Total number of failed predictions')

# 4-6: Gauge Metrics
MODEL_VERSION = Gauge('ml_model_version', 'Current deployed model version', ['version'])
CHURN_PREDICTED_TOTAL = Gauge('ml_churn_predicted_total', 'Current snapshot of predicted churned users')
ACTIVE_THREADS = Gauge('ml_system_active_threads', 'Number of active inference threads')

# 7-8: Histogram Metrics
REQUEST_LATENCY = Histogram('ml_api_request_latency_seconds', 'Inference request latency in seconds')
MODEL_CONFIDENCE = Histogram('ml_model_confidence_score', 'Confidence score distribution of predictions')

# 9-10: Summary Metrics
MEMORY_USAGE = Summary('ml_system_memory_usage_bytes', 'Summary of memory usage in bytes')
DATA_DRIFT_SCORE = Summary('ml_data_drift_score', 'Summary of feature data drift score over time')

# Set nilai awal untuk versi model
MODEL_VERSION.labels(version='1.0.0').set(1)

# ==============================================================================
# LOGIKA SIMULASI / MONITORING
# ==============================================================================
def fetch_and_monitor():
    # Panggil metrik setelah didefinisikan di atas
    HTTP_REQUESTS.inc()
    
    start_time = time.time()
    try:
        # Simulasi jeda waktu proses model inference
        latency = random.uniform(0.05, 0.4)
        time.sleep(latency)
        
        # Mengisi data ke dalam metrik
        REQUEST_LATENCY.observe(latency)
        SUCCESS_COUNT.inc()
        
        # Simulasi prediksi churn & confidence score
        confidence = random.uniform(0.6, 0.99)
        MODEL_CONFIDENCE.observe(confidence)
        
        if random.choice([0, 1]) == 1:
            CHURN_PREDICTED_TOTAL.inc()
            
        # Simulasi metrik sistem
        ACTIVE_THREADS.set(random.randint(2, 8))
        MEMORY_USAGE.observe(random.uniform(250000000, 300000000)) # ~250-300MB
        DATA_DRIFT_SCORE.observe(random.uniform(0.01, 0.05))
        
    except Exception as e:
        FAILURE_COUNT.inc()
        print(f"Error: {e}")

if __name__ == '__main__':
    # Jalankan server HTTP Prometheus Exporter di port 8000
    start_http_server(8000)
    print("Prometheus Exporter berjalan di http://localhost:8000/metrics")
    
    while True:
        fetch_and_monitor()
        time.sleep(2)