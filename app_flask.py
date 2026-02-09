from flask import Flask, request, render_template, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["student_db"]
collection = db["students"]

@app.route('/')
def index():
    data = collection.find()
    return render_template("student_form.html", students=data)

@app.route('/register', methods=['POST'])
def register():
    student_data = {
    "name": request.form['name'],
    "email": request.form['email'],
    "roll": request.form['roll']
 }

    roll = request.form['roll']
    existing_student = collection.find_one({"roll": roll})
    if existing_student:
          student = {
            "name": request.form['name'],
            "email": request.form['email'],
            "roll": request.form['roll']
            }
          return render_template("student_form.html", student=student, error=f"Roll number {roll} already exists!")
    collection.insert_one(student_data)

    
    data = collection.find()
    return render_template("student_data.html", students=data)


@app.route('/delete/<id>')
def delete_student(id):
    collection.delete_one({"_id": ObjectId(id)})
    data = collection.find()
    return render_template("student_data.html", students=data)
  


@app.route('/edit/<id>')
def edit_student(id):
    student = collection.find_one({"_id": ObjectId(id)})
    return render_template("edit.html", student=student)



@app.route('/update/<id>', methods=['POST'])
def update_student(id):
    # Fetch form data
    name = request.form['name']
    email = request.form['email']
    roll = request.form['roll']

    # Duplicate roll check (ignore current student)
    existing_student = collection.find_one({"roll": roll, "_id": {"$ne": ObjectId(id)}})
    if existing_student:
        # Agar duplicate → wapas edit form render karo with same data
        student = {
            "_id": ObjectId(id),
            "name": name,
            "email": email,
            "roll": roll
        }
        return render_template("edit.html", student=student, error=f"Roll number {roll} already exists!")

    # Update in database
    collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {
            "name": name,
            "email": email,
            "roll": roll
        }}
    )

    # Fetch all students to display
    data = collection.find()
    return render_template("student_data.html", students=data)


if __name__ == "__main__":
    app.run(debug=True)
