import time
import requests
import random
import json

url = "http://192.168.1.20:5001/invocations"

print("Memulai simulasi data inference ke server 192.168.1.20...")

# Contoh data dummy input menyesuaikan fitur preprocessing Churn kamu
headers = {"Content-Type": "application/json"}

print("Memulai simulasi data inference...")

while True:
    # Buat data dummy acak
    dummy_data = {
        "dataframe_records": [
            {
                "Tenure": random.randint(1, 72),
                "MonthlyCharges": random.uniform(20.0, 120.0),
                "TotalCharges": random.uniform(20.0, 8000.0)
            }
        ]
    }
    
    try:
        response = requests.post(url, data=json.dumps(dummy_data), headers=headers)
        print(f"Mengirim data inference. Status: {response.status_code}, Respon: {response.text}")
    except Exception as e:
        print(f"Gagal terhubung ke model server: {e}")
        
    time.sleep(random.uniform(0.5, 2.0))