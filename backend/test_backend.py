import requests
import time

BASE_URL = "http://localhost:8000"

def test_backend():
    print("Testing Backend...")
    
    # 1. Start Journey
    print("1. Starting Journey...")
    start_payload = {
        "user_id": "test-user",
        "start_location": {"lat": 12.9716, "lon": 77.5946},
        "destination": {"lat": 13.0827, "lon": 80.2707},
        "total_distance_km": 350
    }
    try:
        res = requests.post(f"{BASE_URL}/journey/start", json=start_payload)
        res.raise_for_status()
        data = res.json()
        journey_id = data["journey_id"]
        print(f"   Journey Started: {journey_id}")
    except Exception as e:
        print(f"   FAILED to start journey: {e}")
        return

    # 2. Track Journey
    print("2. Tracking Journey...")
    track_payload = {
        "journey_id": journey_id,
        "telemetry": {
            "location": {"lat": 12.9800, "lon": 77.6000},
            "speed_kmph": 60,
            "distance_covered_km": 10
        }
    }
    try:
        res = requests.post(f"{BASE_URL}/journey/track", json=track_payload)
        res.raise_for_status()
        data = res.json()
        print(f"   Tracking OK. ETA: {data.get('eta_iso')}")
    except Exception as e:
        print(f"   FAILED to track journey: {e}")

    # 3. Stop Journey
    print("3. Stopping Journey...")
    stop_payload = {
        "journey_id": journey_id,
        "end_location": {"lat": 13.0000, "lon": 77.7000}
    }
    try:
        res = requests.post(f"{BASE_URL}/journey/stop", json=stop_payload)
        res.raise_for_status()
        print("   Journey Stopped.")
    except Exception as e:
        print(f"   FAILED to stop journey: {e}")

    # 4. Test Breaks
    print("4. Testing Breaks...")
    break_payload = {
        "journey_id": journey_id,
        "total_distance_km": 250,
        "elapsed_time_hours": 3.5
    }
    try:
        res = requests.post(f"{BASE_URL}/breaks/suggest", json=break_payload)
        res.raise_for_status()
        data = res.json()
        print(f"   Break Suggestion: {data['should_take_break']} (Reason: {data.get('reason')})")
    except Exception as e:
        print(f"   FAILED to suggest break: {e}")

    # 5. Test Hotels
    print("5. Testing Hotels...")
    hotel_payload = {
        "lat": 12.9716,
        "lon": 77.5946,
        "radius_km": 5
    }
    try:
        res = requests.post(f"{BASE_URL}/hotels/nearby", json=hotel_payload)
        res.raise_for_status()
        data = res.json()
        hotels = data["hotels"]
        print(f"   Found {len(hotels)} hotels.")
        if hotels:
            hotel_id = hotels[0]["id"]
    except Exception as e:
        print(f"   FAILED to search hotels: {e}")

    # 6. Test SOS
    print("6. Testing SOS...")
    sos_payload = {
        "journey_id": journey_id,
        "location": {"lat": 12.9716, "lon": 77.5946},
        "type": "manual"
    }
    try:
        res = requests.post(f"{BASE_URL}/sos/alert", json=sos_payload)
        res.raise_for_status()
        data = res.json()
        print(f"   SOS Alert Sent: {data['alert_id']}")
    except Exception as e:
        print(f"   FAILED to send SOS: {e}")

    # 7. Test Reviews
    print("7. Testing Reviews...")
    if 'hotel_id' in locals():
        review_payload = {
            "hotel_id": hotel_id,
            "user_id": "test-user",
            "rating": 5,
            "comment": "Great place!",
            "tags": ["family", "clean"]
        }
        try:
            res = requests.post(f"{BASE_URL}/reviews/", json=review_payload)
            res.raise_for_status()
            print("   Review Submitted.")
        except Exception as e:
            print(f"   FAILED to submit review: {e}")

if __name__ == "__main__":
    test_backend()
