import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def verify_ollama():
    url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate").replace("/generate", "/tags")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            models = [m['name'] for m in response.json().get('models', [])]
            target_model = os.getenv("OLLAMA_MODEL", "codellama")
            
            # Check if target model or latest version of it exists
            exists = any(target_model in m for m in models)
            
            if exists:
                print(f"Ollama is linked. Model '{target_model}' found.")
                return True
            else:
                print(f"Ollama is running, but model '{target_model}' not found in {models}")
                return False
        else:
            print(f"Ollama returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"Failed to connect to Ollama: {str(e)}")
        return False

if __name__ == "__main__":
    verify_ollama()
