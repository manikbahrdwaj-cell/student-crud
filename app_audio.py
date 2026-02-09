# =========================
# Python 3.14 Patch for PyDub
# =========================
import sys
import types

# Patch missing pyaudioop module
sys.modules['pyaudioop'] = types.ModuleType('pyaudioop')

# Optional dummy functions to prevent PyDub runtime errors
def dummy_mul(*args, **kwargs): return b''
def dummy_ratecv(*args, **kwargs): return b'', 1

sys.modules['pyaudioop'].mul = dummy_mul
sys.modules['pyaudioop'].ratecv = dummy_ratecv

# =========================
# Imports (after patch)
# =========================
import io
import base64
import numpy as np
import torch
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from bson.objectid import ObjectId
from sentence_transformers import SentenceTransformer
import torchaudio
from pydub import AudioSegment

# =========================
# Configure FFmpeg for PyDub
# =========================
AudioSegment.converter = r"C:\Users\manik.bhardwaj\Downloads\ffmpeg-8.0.1-essentials_build\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\Users\manik.bhardwaj\Downloads\ffmpeg-8.0.1-essentials_build\ffmpeg-8.0.1-essentials_build\bin\ffprobe.exe"

# =========================
# Test audio load (optional)
# =========================
# audio = AudioSegment.from_file("test.webm", format="webm")
# print(f"Audio length (ms): {len(audio)}")

# =========================
# Initialize FastAPI & Templates
# =========================
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# =========================
# Initialize SentenceTransformer
# =========================
model = SentenceTransformer("all-MiniLM-L6-v2")

# =========================
# MongoDB Setup
# =========================
client = MongoClient("mongodb://localhost:27017/")
db = client["student_db"]
collection = db["students"]

# =========================
# Helper Functions
# =========================

# Decode Base64 audio
def decode_audio(audio_base64: str) -> bytes:
    header, audio_str = audio_base64.split(",", 1)
    return base64.b64decode(audio_str)

# Convert audio bytes to MFCC embedding
def audio_to_embedding(audio_bytes: bytes, target_sample_rate=16000):
    # Convert WebM to WAV
    audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format="webm")
    wav_io = io.BytesIO()
    audio_segment.export(wav_io, format="wav")
    wav_io.seek(0)

    # Load waveform
    waveform, sample_rate = torchaudio.load(wav_io)

    # Resample if needed
    if sample_rate != target_sample_rate:
        waveform = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=target_sample_rate)(waveform)

    # Convert to mono
    if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0, keepdim=True)

    # MFCC
    mfcc = torchaudio.transforms.MFCC(sample_rate=target_sample_rate, n_mfcc=40)(waveform)
    embedding = mfcc.mean(dim=2).squeeze().numpy()
    return embedding.tolist()

# Create student description text
def create_student_text(name, email, roll):
    return f"Student name is {name}, email is {email}, roll number is {roll}"

# =========================
# FastAPI Routes
# =========================

@app.get("/")
async def index(request: Request):
    students = collection.find()
    return templates.TemplateResponse(
        "student_form.html",
        {"request": request, "students": students}
    )

@app.post("/register")
async def register(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    roll: str = Form(...),
    audio: str = Form(None)
):
    # Check for existing roll number
    if collection.find_one({"roll": roll}):
        return templates.TemplateResponse(
            "student_form.html",
            {
                "request": request,
                "student": {"name": name, "email": email, "roll": roll},
                "error": f"Roll number {roll} already exists!"
            }
        )

    # Create embeddings
    text_embedding = model.encode(create_student_text(name, email, roll)).tolist()
    audio_embedding = audio_to_embedding(decode_audio(audio)) if audio else None

    # Insert into MongoDB
    collection.insert_one({
        "name": name,
        "email": email,
        "roll": roll,
        "embedding": text_embedding,
        "audio_embedding": audio_embedding
    })

    students = collection.find()
    return templates.TemplateResponse(
        "student_data.html",
        {"request": request, "students": students}
    )

@app.get("/delete/{id}")
async def delete_student(request: Request, id: str):
    collection.delete_one({"_id": ObjectId(id)})
    students = collection.find()
    return templates.TemplateResponse(
        "student_data.html",
        {"request": request, "students": students}
    )

@app.get("/edit/{id}")
async def edit_student(request: Request, id: str):
    student = collection.find_one({"_id": ObjectId(id)})
    return templates.TemplateResponse(
        "edit.html",
        {"request": request, "student": student}
    )

@app.post("/update/{id}")
async def update_student(
    request: Request,
    id: str,
    name: str = Form(...),
    email: str = Form(...),
    roll: str = Form(...),
    audio: str = Form(None)
):
    # Check for duplicate roll number
    if collection.find_one({"roll": roll, "_id": {"$ne": ObjectId(id)}}):
        return templates.TemplateResponse(
            "edit.html",
            {
                "request": request,
                "student": {"_id": ObjectId(id), "name": name, "email": email, "roll": roll},
                "error": f"Roll number {roll} already exists!"
            }
        )

    text_embedding = model.encode(create_student_text(name, email, roll)).tolist()
    audio_embedding = audio_to_embedding(decode_audio(audio)) if audio else None

    # Update student in MongoDB
    collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {
            "name": name,
            "email": email,
            "roll": roll,
            "embedding": text_embedding,
            "audio_embedding": audio_embedding
        }}
    )

    students = collection.find()
    return templates.TemplateResponse(
        "student_data.html",
        {"request": request, "students": students}
    )
