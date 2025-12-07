import sys
import os
import json
from fastapi.testclient import TestClient

from unittest.mock import MagicMock
import sys

# Mock OpenAI client to avoid API key error during import
sys.modules['openai'] = MagicMock()
sys.modules['openai'].OpenAI = MagicMock()

# Add parent directory to path to import backend modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Fix for relative imports inside backend modules when running from tests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from backend.main import app
from backend.qdpx_parser import extract_codes_from_qdpx

client = TestClient(app)

def test_qdpx_import():
    print("\n--- Testing QDPX Import ---")
    file_path = "/Users/reinerfuentesferrada/ONLINE_DS_THEBRIDGE_Rei/PhenomFlow/data/simulated_interviews/suicidio_rv_06_12_25.qdpx"
    
    with open(file_path, "rb") as f:
        response = client.post("/import/qdpx", files={"file": ("test.qdpx", f, "application/octet-stream")})
    
    if response.status_code == 200:
        data = response.json()
        print(f"Success! Extracted {data['count']} codes.")
        print("Sample codes:", json.dumps(data['codes'][:3], indent=2))
        return data['codes']
    else:
        print(f"Failed: {response.status_code} - {response.text}")
        return None

def test_enhanced_analysis(codes):
    print("\n--- Testing Enhanced Analysis with Custom Codes ---")
    
    # Mock interview text
    text = """
    P: Al principio sentí mucho miedo, una presión fuerte en el pecho.
    I: ¿Y luego?
    P: Luego vi el vacío y sentí que me iba hacia adelante, pero no me movía. Era una confusión total.
    """
    
    payload = {
        "text": text,
        "context": {
            "research_question": "Experiencia de suicidio en RV",
            "phenomenological_approach": "Micro-phenomenology"
        },
        "custom_codes": codes
    }
    
    # Note: This will actually call OpenAI, so we expect it to take a moment.
    # For a quick test without burning tokens, we might want to mock service.analyze_with_pipeline
    # But for full verification, we'll let it run (assuming user has API key set).
    
    # We'll just print the payload structure to confirm we are sending it right
    print("Payload prepared with custom codes.")
    
    # To avoid actual API call in this script if not desired, we can stop here.
    # But let's try to import the service function and check if it accepts the arguments.
    from backend.service import analyze_with_pipeline
    import inspect
    sig = inspect.signature(analyze_with_pipeline)
    print(f"Service signature verified: {sig}")
    
    if 'custom_codes' in sig.parameters:
        print("SUCCESS: analyze_with_pipeline accepts custom_codes.")
    else:
        print("FAILURE: analyze_with_pipeline does NOT accept custom_codes.")

if __name__ == "__main__":
    codes = test_qdpx_import()
    if codes:
        test_enhanced_analysis(codes)
