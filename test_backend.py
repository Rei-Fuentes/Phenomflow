import requests
import json

url = "http://localhost:8000/analyze"
headers = {"Content-Type": "application/json"}
data = {
    "text": "I felt a sudden sense of overwhelming joy when I saw the sunrise. It was as if the world was being born again, and I was part of that rebirth. The colors were vibrant, and the air felt crisp on my skin."
}

try:
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Backend Test Successful!")
        print("-" * 20)
        print("Input Text:", data["text"])
        print("-" * 20)
        print("Analysis Result:")
        print(response.json()["result"])
    else:
        print(f"Backend Test Failed with status code: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"An error occurred: {e}")
