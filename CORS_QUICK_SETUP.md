# CORS Configuration - Developer Quick Card

## Copy-Paste Ready Code Snippets

### 1️⃣ JavaScript Fetch (All CRUD Operations)

```javascript
const API_URL = 'http://localhost:8000/api';
const options = {
  headers: { 'Content-Type': 'application/json' },
  credentials: 'include'
};

// GET all students
fetch(`${API_URL}/students`, { method: 'GET', ...options })
  .then(r => r.json()).then(data => console.log(data));

// POST new student
fetch(`${API_URL}/students`, {
  method: 'POST',
  body: JSON.stringify({
    name: 'John Doe',
    email: 'john@example.com',
    roll: 'STU001'
  }),
  ...options
}).then(r => r.json()).then(data => console.log(data));

// PUT update student
fetch(`${API_URL}/students/ID_HERE`, {
  method: 'PUT',
  body: JSON.stringify({ name: 'Updated Name', email: 'new@example.com' }),
  ...options
}).then(r => r.json()).then(data => console.log(data));

// DELETE student
fetch(`${API_URL}/students/ID_HERE`, { method: 'DELETE', ...options })
  .then(r => r.json()).then(data => console.log(data));
```

### 2️⃣ React + Axios (Recommended)

```javascript
// api.js
import axios from 'axios';

export const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  withCredentials: true,
  headers: { 'Content-Type': 'application/json' }
});

// Use in components
import { api } from './api';

// GET
api.get('/students').then(res => console.log(res.data));

// POST
api.post('/students', {
  name: 'John Doe',
  email: 'john@example.com',
  roll: 'STU001'
}).then(res => console.log(res.data));

// PUT
api.put('/students/ID_HERE', {
  name: 'Updated Name'
}).then(res => console.log(res.data));

// DELETE
api.delete('/students/ID_HERE')
  .then(res => console.log(res.data));
```

### 3️⃣ cURL Testing

```bash
# Health check with CORS header
curl -i -H "Origin: http://localhost:3000" http://localhost:8000/api/health

# GET students
curl http://localhost:8000/api/students

# POST student
curl -X POST http://localhost:8000/api/students \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","roll":"STU001"}'

# PUT student (replace ID_HERE)
curl -X PUT http://localhost:8000/api/students/ID_HERE \
  -H "Content-Type: application/json" \
  -d '{"name":"Updated Name"}'

# DELETE student (replace ID_HERE)
curl -X DELETE http://localhost:8000/api/students/ID_HERE
```

### 4️⃣ Python Requests

```python
import requests
import json

API_URL = 'http://localhost:8000/api'
headers = {'Content-Type': 'application/json', 'Origin': 'http://localhost:3000'}

# GET all students
response = requests.get(f'{API_URL}/students', headers=headers)
print(response.json())

# POST new student
student = {
    'name': 'John Doe',
    'email': 'john@example.com',
    'roll': 'STU001'
}
response = requests.post(f'{API_URL}/students', json=student, headers=headers)
print(response.json())

# PUT update
response = requests.put(f'{API_URL}/students/ID_HERE', 
  json={'name': 'Updated Name'}, headers=headers)
print(response.json())

# DELETE
response = requests.delete(f'{API_URL}/students/ID_HERE', headers=headers)
print(response.json())
```

---

## 🚀 Startup Commands

```bash
# Terminal 1: MongoDB
mongod --dbpath /path/to/mongo/data

# Terminal 2: FastAPI Backend
cd c:\Users\manik.bhardwaj\.vscode\python
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000

# Terminal 3: Frontend (optional)
npm start
# or
npm run dev
```

---

## ✅ Configuration Checklist

| Item | Status | Location |
|------|--------|----------|
| CORS Middleware | ✅ | `api.py:45` |
| CORS Config Dict | ✅ | `api.py:40-56` |
| Allowed Origins | ✅ | `.env:5` |
| MongoDB Connection | ✅ | `api.py:65-72` |
| All HTTP Methods | ✅ | `api.py:48` |
| Required Headers | ✅ | `api.py:49-55` |
| Credentials Enabled | ✅ | `api.py:47` |
| Preflight Cache | ✅ | `api.py:56 (600s)` |

---

## 📊 CORS Configuration Overview

```
┌─────────────────────────────────────┐
│      CORS Configuration              │
├─────────────────────────────────────┤
│ Allowed Origins:                    │
│ ✅ http://localhost:3000            │
│ ✅ http://localhost:5173            │
│ ✅ http://localhost:8000            │
├─────────────────────────────────────┤
│ HTTP Methods:                       │
│ ✅ GET, POST, PUT, DELETE, OPTIONS, │
│    PATCH                            │
├─────────────────────────────────────┤
│ Headers:                            │
│ ✅ Content-Type, Authorization,     │
│    Accept, Origin, etc.             │
├─────────────────────────────────────┤
│ Credentials: ✅ Enabled             │
│ Preflight Cache: ✅ 600 seconds     │
└─────────────────────────────────────┘

         ↓ API Running ↓

┌─────────────────────────────────────┐
│      Available Endpoints            │
├─────────────────────────────────────┤
│ GET    /api/health                  │
│ GET    /api/students                │
│ GET    /api/students/{id}           │
│ POST   /api/students                │
│ PUT    /api/students/{id}           │
│ DELETE /api/students/{id}           │
│ PATCH  /api/students/{id}           │
└─────────────────────────────────────┘

         ↓ Frontend ↓

┌─────────────────────────────────────┐
│   React / Vue / Vanilla JS          │
│   (localhost:3000 or 5173)          │
└─────────────────────────────────────┘
```

---

## 🔧 Troubleshooting One-Liners

```bash
# Check API is running
curl http://localhost:8000/api/health

# Check MongoDB
python -c "from pymongo import MongoClient; MongoClient('mongodb://localhost:27017/').admin.command('ping'); print('✅ MongoDB OK')"

# Kill process on port 8000
taskkill /PID $(netstat -ano | findstr :8000 | awk '{print $5}') /F

# Check environment variables
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('ALLOWED_ORIGINS'))"

# Test CORS headers
curl -i -H "Origin: http://localhost:3000" http://localhost:8000/api/students
```

---

## 📚 Documentation Files

| File | Use Case |
|------|----------|
| `.env` | Configuration values |
| `api.py` | Backend implementation |
| `models.py` | Data validation |
| `CORS_CONFIGURATION.md` | Detailed setup guide |
| `CORS_QUICK_REFERENCE.md` | Frontend reference |
| `CORS_TESTING_GUIDE.md` | Testing procedures |
| `CORS_IMPLEMENTATION_COMPLETE.md` | Full overview |

---

## 🎯 Key Points to Remember

1. **CORS is about security** - only allowed origins can access the API
2. **Preflight requests** - OPTIONS requests check if actual request is allowed
3. **Credentials** - `credentials: 'include'` required for cookies/auth
4. **Environment variables** - `.env` controls allowed origins, restart API after changes
5. **Browser cache** - Clear with Ctrl+Shift+Delete if issues persist
6. **Development vs Production** - Different `ALLOWED_ORIGINS` for each

---

## 💡 Pro Tips

✨ Use http://localhost:8000/docs for interactive API testing  
✨ Check Browser DevTools → Network tab for CORS header details  
✨ Use `console.error()` to see actual CORS error messages  
✨ Test with cURL before testing in frontend code  
✨ Always include `Origin` header when testing with cURL  
✨ Don't use wildcard (`*`) for origins in production  

---

**Phase 1 Backend API CORS Configuration ✅ READY**

Create, Read, Update, Delete - All with proper CORS security! 🚀
