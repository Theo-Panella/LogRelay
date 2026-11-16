import requests

payload = {"batch": {'0': ['[Mon Dec 05 16:40:06 2005] [notice] workerEnv.init() ok /etc/httpd/conf/workers2.properties', 'Apache', 'teste-2']}}

#batch={'0': ['[Mon Dec 05 16:40:06 2005] [notice] workerEnv.init() ok /etc/httpd/conf/workers2.properties', 'Apache', 'teste-2']}

response = requests.post("http://localhost:8000", json=payload)

print(response.status_code)