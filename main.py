from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from PIL import Image
import pytesseract
import io
import base64

app = FastAPI(title="Tesseract OCR Service")

class OCRRequest(BaseModel):
    """Schema for the incoming request body."""
    # Base64 encoded image string
    image_base64: str

# Define the endpoint for OCR
@app.post("/ocr")
async def perform_ocr(request: OCRRequest):
    """
    Accepts a base64 string of an image, performs OCR, and returns the text.
    """
    try:
        # 1. Decode Base64 string to bytes
        # The base64 string from n8n might need to be stripped of potential prefixes
        image_data = base64.b64decode(request.image_base64)
        
        # 2. Convert bytes to an in-memory PIL Image object
        image = Image.open(io.BytesIO(image_data))
        
        # 3. Perform OCR
        ocr_text = pytesseract.image_to_string(image)
        
        # 4. Return result
        return {
            "status": "success",
            "extracted_text": ocr_text.strip()
        }
        
    except Exception as e:
        # Log the error internally and return a 500 status to the client
        print(f"OCR Processing Error: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Error processing image for OCR. Check file format or Tesseract configuration."
        )

# Health check endpoint
@app.get("/")
def health_check():
    return {"status": "ok", "service": "Tesseract OCR Microservice"}
