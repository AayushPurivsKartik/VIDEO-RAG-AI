from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from processor import process_video, search_video

app = FastAPI()

# Allow React Frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary storage for uploads
os.makedirs("temp_videos", exist_ok=True)

@app.post("/upload_video")
async def upload_video(file: UploadFile = File(...)):
    file_location = f"temp_videos/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Trigger AI processing
    num_frames = process_video(file_location)
    
    return {"message": "Video processed successfully", "frames_indexed": num_frames}

@app.post("/search")
async def search(query: str = Form(...)):
    results = search_video(query)
    return {"results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


### **Step 5: The Frontend (React)**

# We will build a modern, dark-themed UI. Ensure you have Node.js installed.

# 1.  **Create React App:**
#     ```bash
#     npm create vite@latest frontend -- --template react
#     cd frontend
#     npm install axios lucide-react
#     # Add Tailwind CSS manually if you prefer, or use standard CSS
