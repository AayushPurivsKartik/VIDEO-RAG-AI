import cv2
import chromadb
from ultralytics import YOLO
from sentence_transformers import SentenceTransformer
from PIL import Image
import uuid
import os

# 1. Initialize AI Models
# YOLO for Object Detection (Counting)
yolo_model = YOLO("yolov8n.pt")  # Downloads automatically (Nano model is fast)
# CLIP for Semantic Embeddings (Understanding context)
clip_model = SentenceTransformer('clip-ViT-B-32')

# 2. Initialize Vector DB (ChromaDB)
chroma_client = chromadb.Client()
try:
    collection = chroma_client.get_collection(name="video_frames")
    chroma_client.delete_collection(name="video_frames") # Reset for demo
except:
    pass
collection = chroma_client.create_collection(name="video_frames")

def process_video(video_path: str):
    """
    Reads video, extracts 1 frame/sec, runs AI, and stores data.
    """
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = 0
    results_summary = []

    print(f"Processing {video_path}...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Process only 1 frame per second to save resources
        if frame_count % fps == 0:
            timestamp = frame_count / fps
            
            # Convert BGR (OpenCV) to RGB (Pillow)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)

            # --- AI TASK 1: OBJECT DETECTION (YOLO) ---
            yolo_results = yolo_model(rgb_frame, verbose=False)
            detected_objects = {}
            
            # Count objects (e.g., {'person': 3, 'car': 1})
            for box in yolo_results[0].boxes:
                cls_id = int(box.cls[0])
                label = yolo_model.names[cls_id]
                detected_objects[label] = detected_objects.get(label, 0) + 1

            # --- AI TASK 2: EMBEDDINGS (CLIP) ---
            # Create a vector representation of the image
            embedding = clip_model.encode(pil_image).tolist()

            # --- STORE DATA ---
            # Create a description for metadata
            desc_text = ", ".join([f"{count} {label}" for label, count in detected_objects.items()])
            
            collection.add(
                ids=[str(uuid.uuid4())],
                embeddings=[embedding],
                metadatas=[{
                    "timestamp": timestamp,
                    "objects_json": str(detected_objects), # Store as string for simplicity
                    "description": desc_text
                }],
                documents=[desc_text] # Helpful for debugging
            )
            
            results_summary.append({
                "timestamp": timestamp,
                "objects": detected_objects
            })

        frame_count += 1

    cap.release()
    print("Processing Complete. Indexed in ChromaDB.")
    return len(results_summary)

def search_video(text_query: str, n_results=5):
    """
    Searches the Vector DB for frames matching the text query.
    """
    query_embedding = clip_model.encode(text_query).tolist()
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    # Parse results for frontend
    formatted_results = []
    for i in range(len(results['ids'][0])):
        formatted_results.append({
            "timestamp": results['metadatas'][0][i]['timestamp'],
            "score": results['distances'][0][i], # Lower distance = better match
            "description": results['metadatas'][0][i]['description']
        })
    
    # Sort by timestamp to show progression
    formatted_results.sort(key=lambda x: x['timestamp'])
    return formatted_results