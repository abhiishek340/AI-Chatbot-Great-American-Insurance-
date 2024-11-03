from fastapi import FastAPI, HTTPException, Request, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
import logging
import os
from pathlib import Path
from typing import List
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(
    title="AI Chatbot",
    description="A fast chatbot powered by Gemini-Pro"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the current directory
BASE_DIR = Path(__file__).resolve().parent

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure templates
templates = Jinja2Templates(directory="templates")

# Configure Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
AI_MODEL = os.getenv('AI_MODEL', 'gemini')

try:
    genai.configure(api_key=GOOGLE_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-pro')
    logger.info("Gemini API configured successfully")
except Exception as e:
    logger.error(f"Error configuring Gemini API: {str(e)}")

class ChatMessage(BaseModel):
    message: str

async def get_gemini_response(message: str) -> str:
    try:
        logger.info(f"Sending message to Gemini: {message}")
        
        prompt = f"""You are a knowledgeable customer service representative for Great American Insurance Group.
        When answering questions, provide accurate, well-structured responses about Great American's services.

        Important Information:
        - Founded in 1872
        - "A+" (Superior) rating from A.M. Best
        - Specializes in property and casualty insurance
        - Known for specialty commercial insurance solutions
        - Strong financial stability
        - Excellent claims service
        - Industry-specific expertise
        - Comprehensive coverage options

        Format the response with HTML for better readability:
        <div class='formatted-response'>
            <h2>[Main Topic]</h2>
            <h3>[Subtopic 1]</h3>
            <ul>
                <li>[Detail 1]</li>
                <li>[Detail 2]</li>
            </ul>
            <h3>[Subtopic 2]</h3>
            <ul>
                <li>[Detail 1]</li>
                <li>[Detail 2]</li>
            </ul>
            <p class="contact-info">
                For more information:
                <br>Call: 1-800-545-4269
                <br>Visit: www.greatamericaninsurancegroup.com
            </p>
        </div>

        Question: {message}

        Please provide a detailed, accurate response using the format above."""

        response = gemini_model.generate_content(prompt)
        
        if response.text:
            return response.text
        else:
            return """<div class='formatted-response'>
                     <h2>Contact Great American Insurance Group</h2>
                     <p>For specific information about our services, please contact us:</p>
                     <ul>
                         <li>Phone: 1-800-545-4269</li>
                         <li>Website: www.greatamericaninsurancegroup.com</li>
                         <li>Hours: Monday-Friday, 8:00 AM - 5:00 PM ET</li>
                     </ul>
                     </div>"""
    except Exception as e:
        logger.error(f"Gemini API error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "ai_model": AI_MODEL}
    )

@app.post("/chat")
async def chat(message: ChatMessage):
    try:
        bot_response = await get_gemini_response(message.message)
        return {"response": bot_response}
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Add new class for claim submission
class ClaimSubmission(BaseModel):
    description: str

# Add upload directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Add new endpoint for claim submission
@app.post("/submit-claim")
async def submit_claim(
    description: str = Form(...),
    files: List[UploadFile] = File(None)
):
    try:
        # Create unique directory for this claim
        claim_dir = UPLOAD_DIR / f"claim_{int(time.time())}"
        claim_dir.mkdir(parents=True, exist_ok=True)

        # Save the description
        with open(claim_dir / "description.txt", "w") as f:
            f.write(description)

        # Save uploaded files
        if files:
            for file in files:
                file_path = claim_dir / file.filename
                with open(file_path, "wb") as f:
                    content = await file.read()
                    f.write(content)

        return JSONResponse({
            "message": "Claim submitted successfully",
            "status": "success"
        })

    except Exception as e:
        logger.error(f"Error submitting claim: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Update requirements to include python-multipart
# pip install python-multipart

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)