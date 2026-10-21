import subprocess
import time
import httpx

proc = subprocess.Popen(['/root/albion-analyzer-clone/backend/venv/bin/uvicorn', 'main:app', '--host', '127.0.0.1', '--port', '8000'])
time.sleep(3)
try:
    r = httpx.get('http://127.0.0.1:8000/')
    print('Root:', r.json())
    r2 = httpx.post('http://127.0.0.1:8000/api/scanner/upload', json={'item_id': 'T4_BAG', 'city': 'Bridgewatch', 'price': 5420, 'amount': 12})
    print('Upload:', r2.json())
    r3 = httpx.get('http://127.0.0.1:8000/api/scanner/listings')
    print('Listings:', r3.json())
finally:
    proc.terminate()
    proc.wait()
