import os
from dotenv import load_dotenv
import sys

# Load env
load_dotenv()

print(f"USE_CLAUDE: {os.getenv('USE_CLAUDE')}")
print(f"ANTHROPIC_API_KEY present: {bool(os.getenv('ANTHROPIC_API_KEY'))}")

try:
    import anthropic
    print("✅ anthropic package imported successfully")
except ImportError:
    print("❌ anthropic package NOT found")
    sys.exit(1)

try:
    from backend.service import client, MODEL
    print(f"✅ Service imported. Client type: {type(client)}")
    print(f"✅ Model: {MODEL}")
    
    if isinstance(client, anthropic.Anthropic):
        print("✅ Client is correctly identified as Anthropic")
    else:
        print(f"⚠️ Client is NOT Anthropic (Expected if USE_CLAUDE is false or key missing)")

except Exception as e:
    print(f"❌ Error importing service: {e}")
