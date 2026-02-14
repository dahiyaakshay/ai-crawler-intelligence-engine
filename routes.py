"""
API Routes
----------
Handles:
- Log upload
- Summary retrieval
- Bot listing
- Bot detail view
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from database import Database
from log_parser import parse_log_file
from behavioral_analyzer import analyze_behavior
from bot_detector import detect_bot

router = APIRouter()
db = Database()


# ==========================
# Upload & Process Log File
# ==========================

@router.post("/upload")
async def upload_log(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        lines = contents.decode("utf-8", errors="ignore").splitlines()

        parsed_logs = parse_log_file(lines)

        upload_id = db.create_upload(file.filename, len(lines))

        behavioral_profiles = analyze_behavior(parsed_logs)

        processed_count = 0

        for profile in behavioral_profiles:
            bot_data = detect_bot(profile)
            db.insert_bot(upload_id, bot_data)
            processed_count += 1

        db.update_processed_bots(upload_id, processed_count)

        return {
            "message": "Log processed successfully",
            "upload_id": upload_id,
            "total_lines": len(lines),
            "processed_bots": processed_count
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==========================
# Summary Endpoint
# ==========================

@router.get("/summary")
def get_summary():
    return db.get_summary()


# ==========================
# All Bots
# ==========================

@router.get("/bots")
def get_all_bots():
    return db.get_all_bots()


# ==========================
# Single Bot Details
# ==========================

@router.get("/bot/{bot_id}")
def get_bot(bot_id: str):
    bot = db.get_bot_by_id(bot_id)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    return bot
