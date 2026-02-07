import requests
import json

url = 'http://localhost:8000/api/auth/register'
headers = {'Content-Type': 'application/json'}
data = {
    'nombre': 'Test User',
    'email': 'testuser@example.com',
    'password': 'password123'
}

print(f"Testing registration against {url}...")
try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 201:
        print("✅ Registration successful!")
    elif response.status_code == 400 and 'email ya está registrado' in response.text:
        print("✅ Registration logic works (duplicate check)")
    else:
        print("❌ Registration failed")

except Exception as e:
    print(f"❌ Connection error: {e}")
