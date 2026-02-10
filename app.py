from fastapi import FastAPI, Form, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson.objectid import ObjectId
from sentence_transformers import SentenceTransformer
from pydantic import ValidationError
from models import StudentCreate, StudentUpdate, StudentResponse, ErrorResponse
from dotenv import load_dotenv
import os
from typing import List

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Student Registration API",
    description="REST API for Student CRUD operations with MongoDB",
    version="1.0.0"
)
model = SentenceTransformer("all-MiniLM-L6-v2")

# ==================== CORS Configuration ====================
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "student_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "students")

# MongoDB Connection
try:
    client = MongoClient(MONGODB_URL)
    # Verify the connection
    client.admin.command('ping')
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
except PyMongoError as e:
    print(f"MongoDB Connection Error: {e}")
    raise

   



def create_student_text(name, email, roll):
    return f"Student name is {name}, email is {email}, roll number is {roll}"


# ==================== REST API Endpoints (Phase 1) ====================

@app.get("/", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Student Registration API is running"}


@app.post("/api/students", response_model=StudentResponse, status_code=status.HTTP_201_CREATED, tags=["Students"])
async def create_student(student: StudentCreate):
    """
    Create a new student
    
    - **name**: Student's full name (required)
    - **email**: Student's email address (required)
    - **roll**: Student's roll number (required, must be unique)
    """
    try:
        # Check if roll number already exists
        existing_student = collection.find_one({"roll": student.roll})
        if existing_student:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Roll number '{student.roll}' already exists"
            )
        
        # Create text embedding for the student
        text = create_student_text(student.name, student.email, student.roll)
        embedding = model.encode(text).tolist()
        
        # Prepare student document
        student_doc = {
            "name": student.name,
            "email": student.email,
            "roll": student.roll,
            "embedding": embedding
        }
        
        # Insert into MongoDB
        result = collection.insert_one(student_doc)
        
        # Return the created student with ID
        student_doc["_id"] = str(result.inserted_id)
        return student_doc
        
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )


@app.get("/api/students", response_model=List[StudentResponse], tags=["Students"])
async def get_all_students():
    """
    Fetch all students from the database
    
    Returns a list of all students with their details
    """
    try:
        students = []
        cursor = collection.find()
        for student in cursor:
            student["_id"] = str(student["_id"])
            students.append(student)
        return students
    except PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )


@app.get("/api/students/{student_id}", response_model=StudentResponse, tags=["Students"])
async def get_student(student_id: str):
    """
    Fetch a single student by ID
    
    - **student_id**: MongoDB ObjectId of the student
    """
    try:
        # Validate ObjectId format
        if not ObjectId.is_valid(student_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid student ID format"
            )
        
        student = collection.find_one({"_id": ObjectId(student_id)})
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID '{student_id}' not found"
            )
        
        student["_id"] = str(student["_id"])
        return student
        
    except PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )


@app.put("/api/students/{student_id}", response_model=StudentResponse, tags=["Students"])
async def update_student(student_id: str, student_update: StudentUpdate):
    """
    Update a student's information
    
    - **student_id**: MongoDB ObjectId of the student
    - **name**: Student's full name (optional)
    - **email**: Student's email address (optional)
    - **roll**: Student's roll number (optional)
    """
    try:
        # Validate ObjectId format
        if not ObjectId.is_valid(student_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid student ID format"
            )
        
        # Check if student exists
        existing_student = collection.find_one({"_id": ObjectId(student_id)})
        if not existing_student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID '{student_id}' not found"
            )
        
        # Prepare update data (only non-None fields)
        update_data = {}
        if student_update.name is not None:
            update_data["name"] = student_update.name
        if student_update.email is not None:
            update_data["email"] = student_update.email
        if student_update.roll is not None:
            update_data["roll"] = student_update.roll
        
        # If no fields to update, return the existing student
        if not update_data:
            existing_student["_id"] = str(existing_student["_id"])
            return existing_student
        
        # Check for duplicate roll number if roll is being updated
        if "roll" in update_data:
            duplicate = collection.find_one({
                "roll": update_data["roll"],
                "_id": {"$ne": ObjectId(student_id)}
            })
            if duplicate:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Roll number '{update_data['roll']}' already exists"
                )
        
        # Generate new embedding if name, email, or roll changed
        if update_data:
            updated_student = existing_student.copy()
            updated_student.update(update_data)
            text = create_student_text(
                updated_student.get("name", existing_student.get("name")),
                updated_student.get("email", existing_student.get("email")),
                updated_student.get("roll", existing_student.get("roll"))
            )
            update_data["embedding"] = model.encode(text).tolist()
        
        # Update the student
        collection.update_one(
            {"_id": ObjectId(student_id)},
            {"$set": update_data}
        )
        
        # Return the updated student
        updated_student = collection.find_one({"_id": ObjectId(student_id)})
        updated_student["_id"] = str(updated_student["_id"])
        return updated_student
        
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )


@app.delete("/api/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Students"])
async def delete_student(student_id: str):
    """
    Delete a student by ID
    
    - **student_id**: MongoDB ObjectId of the student
    """
    try:
        # Validate ObjectId format
        if not ObjectId.is_valid(student_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid student ID format"
            )
        
        # Check if student exists
        existing_student = collection.find_one({"_id": ObjectId(student_id)})
        if not existing_student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with ID '{student_id}' not found"
            )
        
        # Delete the student
        collection.delete_one({"_id": ObjectId(student_id)})
        
    except PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )


# ==================== Legacy Template-Based Endpoints (for backward compatibility) ====================

@app.get("/home", tags=["Legacy"])
async def index(request: Request):
    """Legacy endpoint - use /api/students for REST API"""
    data = collection.find()
    return templates.TemplateResponse(
        "student_form.html",
        {"request": request, "students": data}
    )


@app.post("/register", tags=["Legacy"])
async def register(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    roll: str = Form(...),
    audio: str = Form(None)
):
    existing_student = collection.find_one({"roll": roll})
    if existing_student:
        student = {"name": name, "email": email, "roll": roll}
        return templates.TemplateResponse(
            "student_form.html",
            {
                "request": request,
                "student": student,
                "error": f"Roll number {roll} already exists!"
            }
        )

    text = create_student_text(name, email, roll)
    embedding_text = model.encode(text).tolist()
    
    collection.insert_one({
        "name": name,
        "email": email,
        "roll": roll,
        "embedding": embedding_text
    })

    data = collection.find()
    return templates.TemplateResponse(
        "student_data.html",
        {"request": request, "students": data}
    )


@app.get("/delete/{id}", tags=["Legacy"])
async def delete_student_legacy(request: Request, id: str):
    collection.delete_one({"_id": ObjectId(id)})
    data = collection.find()
    return templates.TemplateResponse(
        "student_data.html",
        {"request": request, "students": data}
    )


@app.get("/edit/{id}", tags=["Legacy"])
async def edit_student_legacy(request: Request, id: str):
    student = collection.find_one({"_id": ObjectId(id)})
    return templates.TemplateResponse(
        "edit.html",
        {"request": request, "student": student}
    )


@app.post("/update/{id}", tags=["Legacy"])
async def update_student_legacy(
    request: Request,
    id: str,
    name: str = Form(...),
    email: str = Form(...),
    roll: str = Form(...),
    audio: str = Form(None)
):
    existing_student = collection.find_one({
        "roll": roll,
        "_id": {"$ne": ObjectId(id)}
    })

    if existing_student:
        student = {
            "_id": ObjectId(id),
            "name": name,
            "email": email,
            "roll": roll
        }
        return templates.TemplateResponse(
            "edit.html",
            {
                "request": request,
                "student": student,
                "error": f"Roll number {roll} already exists!"
            }
        )
    text = create_student_text(name, email, roll)
    embedding = model.encode(text).tolist()
    

    collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"name": name, "email": email, "roll": roll,"embedding": embedding}}
    )

    data = collection.find()
    return templates.TemplateResponse(
        "student_data.html",
        {"request": request, "students": data}
    )
