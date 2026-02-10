# Phase 3.1: API Service Layer - Quick Reference Guide

## 🚀 Quick Start

### Basic Usage in Components

```javascript
import { createStudent, getStudents, deleteStudent } from '@/services/api';

// Create a student
const newStudent = await createStudent({
  name: 'John Doe',
  email: 'john@example.com',
  roll: 'CS001'
});

// Get all students
const students = await getStudents();

// Delete a student
await deleteStudent(studentId);
```

---

## 📋 API Methods Reference

| Method | Endpoint | HTTP Method | Purpose |
|--------|----------|-------------|---------|
| `createStudent(data)` | `/students` | POST | Create new student |
| `getStudents()` | `/students` | GET | Fetch all students |
| `getStudent(id)` | `/students/{id}` | GET | Fetch single student |
| `updateStudent(id, data)` | `/students/{id}` | PUT | Update student |
| `deleteStudent(id)` | `/students/{id}` | DELETE | Delete student |

---

## 💡 Common Patterns

### Pattern 1: Fetch Data on Component Mount
```javascript
import { useEffect, useState } from 'react';
import { getStudents } from '@/services/api';

function StudentList() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const data = await getStudents();
        setStudents(data);
      } catch (err) {
        console.error('Failed to load students:', err.message);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  return loading ? <div>Loading...</div> : <div>{/* render */}</div>;
}
```

### Pattern 2: Handle Form Submission
```javascript
import { createStudent } from '@/services/api';

async function handleSubmit(formData) {
  try {
    const result = await createStudent(formData);
    console.log('Created:', result);
    // Redirect or update state
  } catch (error) {
    console.error('Error:', error.message);
    // Show error to user
  }
}
```

### Pattern 3: Handle Errors by Status Code
```javascript
import { updateStudent } from '@/services/api';

try {
  await updateStudent(id, data);
} catch (error) {
  switch (error.status) {
    case 404:
      console.log('Student not found');
      break;
    case 422:
      console.log('Validation error:', error.detail);
      break;
    case 409:
      console.log('Roll number already exists');
      break;
    default:
      console.log('Error:', error.message);
  }
}
```

---

## 🔧 Configuration

### Environment Variables
File: `.env.local`

```env
# API Base URL (change for production)
REACT_APP_API_BASE_URL=http://localhost:8000/api

# Environment mode (affects logging)
REACT_APP_ENV=development
```

### Change API Base URL
Edit `.env.local`:
```env
REACT_APP_API_BASE_URL=https://your-api.com/api
```

Then restart the React dev server.

---

## 🛠️ Utility Functions

### Check API Health
```javascript
import { checkApiHealth } from '@/services/api';

const isOnline = await checkApiHealth();
if (isOnline) {
  console.log('API is accessible');
}
```

### Get API URL
```javascript
import { getApiBaseUrl } from '@/services/api';

console.log(`Using: ${getApiBaseUrl()}`);
```

### Add Custom Header
```javascript
import { setApiHeader } from '@/services/api';

// For authentication in future
setApiHeader('Authorization', `Bearer ${token}`);
```

### Remove Custom Header
```javascript
import { removeApiHeader } from '@/services/api';

removeApiHeader('Authorization');
```

---

## 📊 Error Response Format

All errors have this structure:

```javascript
{
  status: 400,           // HTTP status code
  message: "...",        // User-friendly message
  detail: {...},         // Detailed info from server
  originalError: Error   // Original error object
}
```

### Common HTTP Status Codes

| Status | Meaning | Action |
|--------|---------|--------|
| 201 | Created | Success - record created |
| 200 | OK | Success - data returned/updated |
| 204 | No Content | Success - deleted |
| 400 | Bad Request | Check input format |
| 404 | Not Found | Student doesn't exist |
| 409 | Conflict | Roll number already exists |
| 422 | Validation Error | Invalid field values |
| 500 | Server Error | Backend issue |

---

## 🧪 Testing

### Mock API for Tests
```javascript
jest.mock('@/services/api', () => ({
  getStudents: jest.fn(() => Promise.resolve([
    { id: '1', name: 'John', email: 'john@example.com', roll: 'CS001' }
  ])),
  createStudent: jest.fn(() => Promise.resolve({ id: '2', name: 'Jane' })),
  deleteStudent: jest.fn(() => Promise.resolve(true)),
}));
```

### Using Real API in Development
Just call the methods directly - they'll hit your local backend.

---

## 🔍 Debugging

### Enable Request/Response Logging
Logs are automatically enabled when `REACT_APP_ENV=development`

In browser console, you'll see:
```
[API] POST /students {name: "...", email: "...", roll: "..."}
[API] Response 201: {id: "...", name: "...", ...}
```

### Check Network Tab
Open DevTools → Network tab to see:
- Request URL
- Request/Response headers
- Request/Response body
- Response status code

### Test Direct API Call
```javascript
// In browser console
import api from '@/services/api';
api.getStudents().then(console.log).catch(console.error);
```

---

## ⚠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| "No response from server" | Start backend: `uvicorn app:app --reload` |
| CORS error | Check `REACT_APP_API_BASE_URL` matches backend CORS config |
| 404 errors | Verify student ID format is valid ObjectId |
| 422 errors | Check field validation (name length, email format, etc.) |
| 409 conflict | Roll number must be unique |
| Timeout errors | Check backend health, may be overloaded |

---

## 📚 Related Documentation

- [Full API Service Documentation](./PHASE_3_1_API_SERVICE_LAYER.md)
- [Backend API Docs](../API_DOCUMENTATION.md)
- [React Migration Plan](../REACT_MIGRATION_PLAN.md)

---

## Next Phase

Once this API Service Layer is working:
1. **Phase 3.2**: Build StudentForm component
2. **Phase 3.3**: Build StudentList component  
3. **Phase 3.4**: Build EditForm component

Each component will import and use methods from this API service layer.

---

**Created**: February 10, 2026  
**Version**: 1.0  
**Status**: ✅ Ready for Use
