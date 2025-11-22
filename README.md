**Phase 1: Start the Engines**

1.  **Terminal 1 (Backend):**
    * Run: `cd backend`
    * Run: `pip install -r requirements.txt` (Only need to do this once)
    * Run: `python main.py`
    * **Check:** Does it say "Application startup complete"? If yes, leave this terminal open.

2.  **Terminal 2 (Frontend):**
    * Run: `cd frontend`
    * Run: `npm install` (Only need to do this once)
    * Run: `npm run dev`
    * **Check:** Does it give you a URL like `http://localhost:5173`?

**Phase 2: The "Hello World" Test**
1.  Go to `http://localhost:5173` in Chrome/Edge.
2.  Upload a **short** video (10-30 seconds is best for a quick test).
3.  **Crucial Step:** Look at your **Backend Terminal** while it uploads. You should see text scrolling by showing that frames are being processed.

4.  If the text stops scrolling and the UI says "Ready", try searching "person". If you get results, you are done!
