MODEL_URL = "http://192.168.1.20:5001/invocations"

print("Prometheus Exporter berjalan di http://localhost:8000/metrics")

while True:
    HTTP_REQUESTS.inc()
    
    # Update Metrik Sistem Lokal
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.virtual_memory().percent)
    DISK_USAGE.set(psutil.disk_usage('/').percent)
    NETWORK_SENT.inc(psutil.net_io_counters().bytes_sent)
    NETWORK_RECV.inc(psutil.net_io_counters().bytes_recv)
    
    # Cek Status Ketersediaan Model Serving Remote
    try:
        # Menembak ke port 5001 milik server Ubuntu
        status_check = requests.get("http://192.168.1.20:5001/version", timeout=2)
        MODEL_AVAILABILITY.set(1 if status_check.status_code == 200 else 0)
    except:
        MODEL_AVAILABILITY.set(0)
        
    time.sleep(1)