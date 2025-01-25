from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
from whatsapp_analyzer import ChatAnalysisService

app = FastAPI(title="WhatsApp Chat Analyzer API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Example heart emojis - copied from main.py
heart_emojis = {
    '❤️', '🧡', '💛', '💚', '💙', '💜', '🖤', '🤍', '🤎', '💔', '❤️‍🔥', '❤️‍🩹', '♥️', '💗'
}

@app.post("/analyze")
async def analyze_chat(file: UploadFile = File(...)):
    """
    Endpoint to analyze a WhatsApp chat file.
    Accepts a chat file upload and returns the analysis results.
    """
    # Create a temporary file to store the upload
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_file_path = temp_file.name

    try:
        # Initialize and run the analysis service
        service = ChatAnalysisService(temp_file_path, heart_emojis)
        service.analyze()
        
        # Get the analysis results
        results = service.get_results()
        
        # Clean up the temporary file
        os.unlink(temp_file_path)
        
        return results
    except Exception as e:
        # Clean up the temporary file in case of error
        os.unlink(temp_file_path)
        raise Exception(f"Error analyzing chat file: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint that returns API information."""
    return {
        "message": "WhatsApp Chat Analyzer API",
        "usage": "POST /analyze with a chat file to analyze WhatsApp conversations"
    } 