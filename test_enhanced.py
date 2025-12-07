import requests
import json

url = "http://localhost:8000/analyze/enhanced"
headers = {"Content-Type": "application/json"}

text = "I felt a sudden sense of overwhelming joy when I saw the sunrise. It was as if the world was being born again, and I was part of that rebirth. The colors were vibrant, and the air felt crisp on my skin."

data = {"text": text}

try:
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Enhanced Analysis Test Successful!")
        print("=" * 80)
        result = response.json()
        
        print("\n📊 PHASE 1: OPEN CODING")
        print("-" * 80)
        print(json.dumps(result.get("phase1_codes", {}), indent=2))
        
        print("\n⏱️  PHASE 2: DIACHRONIC STRUCTURE")
        print("-" * 80)
        print(json.dumps(result.get("phase2_diachronic", {}), indent=2))
        
        print("\n🔄 PHASE 3: SYNCHRONIC STRUCTURE")
        print("-" * 80)
        print(json.dumps(result.get("phase3_synchronic", {}), indent=2))
        
        print("\n💎 PHASE 4: INVARIANTS")
        print("-" * 80)
        print(json.dumps(result.get("phase4_invariants", {}), indent=2))
        
        print("\n📈 PHASE 5: VISUALIZATIONS")
        print("-" * 80)
        viz = result.get("phase5_visualizations", {})
        print("Mermaid Diagram:")
        print(viz.get("mermaid_diagram", ""))
        
    else:
        print(f"Test Failed with status code: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"An error occurred: {e}")
