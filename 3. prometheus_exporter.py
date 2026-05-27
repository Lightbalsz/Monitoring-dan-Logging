import time
import random
import threading
from prometheus_client import start_http_server, Counter, Gauge, Histogram, Summary

# ==============================================================================
# DEFINISI METRIK (10 METRIK BERBEDA)
# ==============================================================================
HTTP_REQUESTS = Counter('ml_api_requests_total', 'Total number of inference requests')
SUCCESS_COUNT = Counter('ml_api_success_total', 'Total number of successful predictions')
FAILURE_COUNT = Counter('ml_api_failure_total', 'Total number of failed predictions')

MODEL_VERSION = Gauge('ml_model_version', 'Current deployed model version', ['version'])
CHURN_PREDICTED_TOTAL = Gauge('ml_churn_predicted_total', 'Current snapshot of predicted churned users')
ACTIVE_THREADS = Gauge('ml_system_active_threads', 'Number of active inference threads')

REQUEST_LATENCY = Histogram('ml_api_request_latency_seconds', 'Inference request latency in seconds')
MODEL_CONFIDENCE = Histogram('ml_model_confidence_score', 'Confidence score distribution of predictions')

MEMORY_USAGE = Summary('ml_system_memory_usage_bytes', 'Summary of memory usage in bytes')
DATA_DRIFT_SCORE = Summary('ml_data_drift_score', 'Summary of feature data drift score over time')

MODEL_VERSION.labels(version='1.0.0').set(1)

# ==============================================================================
# LOGIKA UPDATE METRIK DI BACKGROUND THREAD
# ==============================================================================
def update_metrics_loop():
    while True:
        HTTP_REQUESTS.inc()
        try:
            # Simulasi pemrosesan model
            latency = random.uniform(0.05, 0.2)
            time.sleep(latency)
            
            # Mengisi data metrik
            REQUEST_LATENCY.observe(latency)
            SUCCESS_COUNT.inc()
            
            confidence = random.uniform(0.6, 0.99)
            MODEL_CONFIDENCE.observe(confidence)
            
            if random.choice([0, 1]) == 1:
                CHURN_PREDICTED_TOTAL.inc()
                
            ACTIVE_THREADS.set(random.randint(2, 8))
            MEMORY_USAGE.observe(random.uniform(250000000, 300000000))
            DATA_DRIFT_SCORE.observe(random.uniform(0.01, 0.05))
            
        except Exception as e:
            FAILURE_COUNT.inc()
            print(f"Error: {e}")
            
        # Berikan jeda antar-simulasi update data
        time.sleep(1)

if __name__ == '__main__':
    # 1. Jalankan server HTTP Exporter (Akan langsung merespons jika di-scrape)
    start_http_server(8000)
    print("Prometheus Exporter berjalan di http://localhost:8000/metrics")
    
    # 2. Jalankan background thread untuk menggerakkan data metrik
    updater_thread = threading.Thread(target=update_metrics_loop, daemon=True)
    updater_thread.start()
    
    # 3. Jaga agar main program tetap hidup
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExporter dihentikan.")