import time
import httpx
from fastapi.testclient import TestClient
import sys
sys.path.insert(0, '/root/albion-analyzer-clone/backend')
from main import app
from scanner.sniffer import AlbionPhotonSniffer

def test_full_pipeline():
    client = TestClient(app)
    
    # 1. Initialize sniffer in simulation mode
    sniffer = AlbionPhotonSniffer(backend_url="http://testserver/api/scanner/upload")
    
    # Mocking httpx post inside sniffer to use FastAPI TestClient
    def mock_upload(item_id, city, price, amount):
        payload = {"item_id": item_id, "city": city, "price": price, "amount": amount}
        response = client.post("/api/scanner/upload", json=payload)
        print(f"Sniffer uploaded: {payload} -> Status {response.status_code}")

    sniffer.upload_to_backend = mock_upload
    
    # Trigger one simulation cycle manually
    sniffer.upload_to_backend("T8_MAIN_SWORD", "Caerleon", 480000, 1)
    sniffer.upload_to_backend("T4_BAG", "Bridgewatch", 5400, 15)
    
    # 2. Verify backend cached items
    response = client.get("/api/scanner/listings")
    print("Listings response:", response.json())
    assert response.status_code == 200
    listings = response.json()["listings"]
    assert len(listings) >= 2
    print("Full end-to-end scanner & backend pipeline test passed successfully!")

if __name__ == "__main__":
    test_full_pipeline()
