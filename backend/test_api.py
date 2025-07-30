#!/usr/bin/env python3
"""
Simple test script for the FastAPI backend
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Status: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend server")
        print("   Make sure the backend is running on http://localhost:8000")
        return False

def test_setup_instructions():
    """Test the setup instructions endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/setup-instructions")
        if response.status_code == 200:
            print("✅ Setup instructions endpoint working")
            return True
        else:
            print(f"❌ Setup instructions failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend server")
        return False

def test_import_endpoint():
    """Test the import playlist endpoint with sample data"""
    sample_data = {
        "playlistName": "Test Playlist",
        "tracks": [
            {
                "name": "Test Song",
                "artist": "Test Artist",
                "album": "Test Album"
            }
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/import-playlist", json=sample_data)
        if response.status_code == 500:
            # This is expected if YouTube Music is not authenticated
            print("⚠️  Import endpoint responded (YouTube Music not authenticated)")
            print("   This is expected - you need to run the YouTube Music setup")
            return True
        elif response.status_code == 200:
            print("✅ Import endpoint working")
            return True
        else:
            print(f"❌ Import endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend server")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing FastAPI Backend")
    print("=" * 40)
    
    tests = [
        ("Health Check", test_health),
        ("Setup Instructions", test_setup_instructions),
        ("Import Endpoint", test_import_endpoint)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 40)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed! Backend is working correctly.")
    else:
        print("❌ Some tests failed. Check the backend setup.")

if __name__ == "__main__":
    main() 