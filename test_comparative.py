import requests
import json

url = "http://localhost:8000/analyze/comparative"
headers = {"Content-Type": "application/json"}

text1 = "I felt a sudden sense of overwhelming joy when I saw the sunrise. It was as if the world was being born again, and I was part of that rebirth. The colors were vibrant, and the air felt crisp on my skin."
text2 = "Walking through the forest, I suddenly stopped. The light filtering through the leaves created a pattern that filled me with peace. I felt connected to everything around me, a deep sense of unity with nature."
text3 = "It happened when I looked at the ocean. The vastness of the blue water made me feel small but also infinite. A wave of happiness washed over me, and for a moment, I forgot all my worries."

data = {
    "texts": [text1, text2, text3]
}

try:
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Comparative Analysis Test Successful!")
        print("-" * 20)
        print("Analysis Result:")
        print(response.json()["result"])
    else:
        print(f"Test Failed with status code: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"An error occurred: {e}")
