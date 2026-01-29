import requests
import json
import os
import sys
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "codellama")
OUTPUT_DIR = os.getenv("CONVERTED_OUTPUT_DIR", "./converted_output")

PROMPT_TEMPLATE = """
You are an expert test automation engineer. 
Convert the following Selenium Java (TestNG) code into Playwright JavaScript/TypeScript code.

Rules:
1. Prioritize readability over strict 1:1 mapping.
2. Use modern Playwright locators (e.g., page.locator, getByRole).
3. Ensure all actions are awaited.
4. Convert TestNG annotations (@Test, @BeforeMethod, etc.) to Playwright hooks (test, test.beforeEach, etc.).
5. Provide ONLY the converted code. Do not include explanations or markdown formatting like ```typescript.

### Selenium Java Code:
{source_code}

### Playwright Output:
"""

def convert_code(source_code):
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": PROMPT_TEMPLATE.format(source_code=source_code),
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        converted_code = result.get("response", "").strip()
        
        # Strip potential markdown backticks if the model ignored instructions
        if converted_code.startswith("```"):
            lines = converted_code.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            converted_code = "\n".join(lines).strip()
            
        return converted_code
    except Exception as e:
        return f"Error during conversion: {str(e)}"

def save_output(code, filename="converted_test.spec.ts"):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)
    return filepath

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python converter.py <source_code_file_or_string>")
        sys.exit(1)
    
    input_data = sys.argv[1]
    
    # Check if input is a file path
    if os.path.isfile(input_data):
        with open(input_data, "r") as f:
            source = f.read()
    else:
        source = input_data
        
    print(f"--- Converting to {OLLAMA_MODEL} ---")
    converted = convert_code(source)
    print("--- Conversion Complete ---")
    
    path = save_output(converted)
    print(f"Saved to: {path}")
    print("\nPreview:\n" + converted[:500] + "...")
