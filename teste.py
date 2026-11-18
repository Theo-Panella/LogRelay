import requests
import os
from dotenv import load_dotenv
import hashlib
import hmac

load_dotenv()
secret_key = os.getenv("SECRET_KEY")

payload = {"batch": {'0': ['[Mon Dec 05 16:40:06 2005] [notice] workerEnv.init() ok /etc/httpd/conf/workers2.properties', 'Apache', 'teste-2']}}
assinatura = hmac.new(secret_key, payload, hashlib.sha256).hexdigest()

headers = {
    "Authorization": secret_key,
    "Signature" : assinatura
}

response = requests.post("http://localhost:8000", json=payload, headers=headers)

print(response.status_code)