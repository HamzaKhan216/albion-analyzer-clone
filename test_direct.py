import sys
sys.path.insert(0, '/root/albion-analyzer-clone/backend')

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_endpoints():
    # 1. Test root
    r1 = client.get("/")
    print("GET / ->", r1.status_code, r1.json())
    assert r1.status_code == 200

    # 2. Test uploading private scanner data
    sample_data = {
        "item_id": "T4_BAG",
        "city": "Bridgewatch",
        "price": 5420,
        "amount": 12
    }
    r2 = client.post("/api/scanner/upload", json=sample_data)
    print("POST /api/scanner/upload ->", r2.status_code, r2.json())
    assert r2.status_code == 200
    assert r2.json()["status"] == "success"

    # 3. Test listing private scanned data
    r3 = client.get("/api/scanner/listings")
    print("GET /api/scanner/listings ->", r3.status_code, r3.json())
    assert r3.status_code == 200
    assert len(r3.json()["listings"]) == 1

if __name__ == "__main__":
    test_endpoints()
    print("All unit tests passed successfully!")
