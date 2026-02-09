

from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from bson.objectid import ObjectId
from sentence_transformers import SentenceTransformer

app = FastAPI()
model = SentenceTransformer("all-MiniLM-L6-v2")


templates = Jinja2Templates(directory="templates")


client = MongoClient("mongodb://localhost:27017/")
db = client["student_db"]
collection = db["students"]

   



def create_student_text(name, email, roll):
    return f"Student name is {name}, email is {email}, roll number is {roll}"



@app.get("/")
async def index(request: Request):
    data = collection.find()
    return templates.TemplateResponse(
        "student_form.html",
        {"request": request, "students": data}
    )


@app.post("/register")
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


@app.get("/delete/{id}")
async def delete_student(request: Request, id: str):
    collection.delete_one({"_id": ObjectId(id)})
    data = collection.find()
    return templates.TemplateResponse(
        "student_data.html",
        {"request": request, "students": data}
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
