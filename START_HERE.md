# 🚀 START HERE - Phase 1 Backend Setup

## Quick Setup (5 Minutes)

### Step 1️⃣: Install Dependencies
```bash
pip install -r requirements.txt
```
⏱️ Takes ~2 minutes

### Step 2️⃣: Start MongoDB
```bash
mongod
```
Or skip if using MongoDB Atlas (then update `.env`)

### Step 3️⃣: Start the API
```bash
uvicorn api:app --reload
```

### Step 4️⃣: Test It
Open in browser:
```
http://localhost:8000/docs
```

---

## ✅ You're Ready!

Try the interactive API in the browser - create, read, update, delete students.

---

## 📋 Configuration

All configured in `.env`:
- MongoDB: `mongodb://localhost:27017/`
- Database: `student_db`
- API Port: `8000`
- CORS: `localhost:3000, localhost:5173, localhost:8000`

**To change**: Edit `.env` and restart API.

---

## 📚 Learn More

- **Full Guide**: `PHASE_1_SETUP_GUIDE.md`
- **Configuration**: `PHASE_1_CONFIG_COMPLETE.md`
- **Implementation**: `PHASE_1_COMPLETION_VERIFIED.md`
- **API Browser**: http://localhost:8000/docs

---

## 🧪 Test Endpoints

### Health Check
```bash
curl http://localhost:8000/api/health
```

### Create Student
```bash
curl -X POST http://localhost:8000/api/students \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","roll":"CS001"}'
```

### Get All Students
```bash
curl http://localhost:8000/api/students
```

---

**Everything Works?** ✅

You have a **fully functional REST API**!

Next: Connect your React/Vite frontend to these endpoints.
