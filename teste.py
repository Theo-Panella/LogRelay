import requests
import os
from dotenv import load_dotenv
import hashlib
import hmac
import base64
import json
from datetime import datetime, timezone

load_dotenv()
secret_key = os.getenv("SECRET_KEY")

payload = {
    "batch" : { 
        "0": ["[Sun Dec 04 06:43:34 2005] [notice] workerEnv.init() ok /etc/httpd/conf/workers2.properties", "Apache", "teste-2"], 
        "1": ["[Sun Dec 04 06:43:34 2005] [notice] workerEnv.init() ok /etc/httpd/conf/workers2.properties", "Apache", "teste-2"], 
        "2": ["[Sun Dec 04 06:43:34 2005] [notice] workerEnv.init() ok /etc/httpd/conf/workers2.properties", "Apache", "teste-2"], 
        "3": ["[Sun Dec 04 06:45:50 2005] [notice] workerEnv.init() ok /etc/httpd/conf/workers2.properties", "Apache", "teste-2"], 
        "4": ["[Sun Dec 04 06:45:50 2005] [notice] workerEnv.init() ok /etc/httpd/conf/workers2.properties", "Apache", "teste-2"], 
        "5": ["[Sun Dec 04 06:46:30 2005] [notice] workerEnv.init() ok /etc/httpd/conf/workers2.properties", "Apache", "teste-2"], 
        "6": ["[Sun Dec 04 06:46:30 2005] [notice] workerEnv.init() ok /etc/httpd/conf/workers2.properties", "Apache", "teste-2"]
    }
}
time_stamp = datetime.now(timezone.utc).isoformat()
payload_utf8, secret_key_utf8 = (json.dumps(payload).encode("utf8") + time_stamp.encode("utf8")) , (secret_key.encode("utf8"))
assinatura = hmac.new(secret_key_utf8, payload_utf8, hashlib.sha256).hexdigest()

headers = {
    "TimeStamp": time_stamp,
    "Signature" : assinatura
}

response = requests.post("http://localhost:8000", json=payload, headers=headers)

print(response.status_code)
print(f"assinatura: {assinatura}")