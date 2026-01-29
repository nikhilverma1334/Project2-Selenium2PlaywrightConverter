from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import httpx
import time
import os
import json
from dotenv import load_dotenv
import uvicorn
import logging

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Data Schema for Request
class ConversionRequest(BaseModel):
    source_code: str
    target_language: str = "TypeScript"
    model: str = os.getenv("OLLAMA_MODEL", "codellama")

# Ollama Config
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "codellama")

PROMPT_TEMPLATE = """
You are an expert test automation engineer. 
Convert the following Selenium Java (TestNG) code into Playwright {target_language} code.

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

@app.get("/api/models")
async def get_models():
    try:
        url = OLLAMA_URL.replace("/generate", "/tags")
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return response.json()
    except Exception as e:
        return {"models": [{"name": "codellama"}]}

@app.post("/api/convert/stream")
async def convert_stream(request: ConversionRequest):
    async def event_generator():
        payload = {
            "model": request.model,
            "prompt": PROMPT_TEMPLATE.format(target_language=request.target_language, source_code=request.source_code),
            "stream": True,
            "options": {
                "temperature": 0.1,
                "num_predict": 1024,
            }
        }
        
        try:
            async with httpx.AsyncClient() as client:
                async with client.stream("POST", OLLAMA_URL, json=payload, timeout=600.0) as response:
                    async for line in response.aiter_lines():
                        if not line:
                            continue
                        data = json.loads(line)
                        if "response" in data:
                            yield data["response"]
                        if data.get("done"):
                            break
        except Exception as e:
            yield f"\n\n[Error: {str(e)}]"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.post("/api/convert")
async def convert(request: ConversionRequest):
    payload = {
        "model": request.model,
        "prompt": PROMPT_TEMPLATE.format(target_language=request.target_language, source_code=request.source_code),
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 1024,
        }
    }
    
    start_time = time.time()
    logger.info(f"Starting conversion with model {request.model}...")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(OLLAMA_URL, json=payload, timeout=600.0)
            response.raise_for_status()
            
        result = response.json()
        converted_code = result.get("response", "").strip()
        
        duration = time.time() - start_time
        logger.info(f"Conversion complete in {duration:.2f} seconds.")
        
        # Clean up code blocks if model ignored "ONLY code" instruction
        if "```" in converted_code:
            parts = converted_code.split("```")
            for part in parts:
                cleaned = part.strip()
                if any(kw in cleaned for kw in ["import", "test", "await", "page."]):
                    # Remove language identifier if present (e.g., "typescript\n")
                    if "\n" in cleaned:
                        first_line = cleaned.split("\n")[0].lower()
                        if first_line in ["typescript", "javascript", "ts", "js"]:
                            converted_code = cleaned.split("\n", 1)[1]
                        else:
                            converted_code = cleaned
                    else:
                        converted_code = cleaned
                    break
        
        return {"converted_code": converted_code.strip(), "duration": duration}
    except Exception as e:
        logger.error(f"Error during conversion: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files for Frontend
app.mount("/", StaticFiles(directory="backend/static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
