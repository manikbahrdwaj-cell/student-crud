# Phase 3.1: API Service Layer Implementation - COMPLETE ✅

## Overview
This document details the implementation of the centralized API Service Layer for Phase 3.1 of the Student Registration System React migration. This layer provides a single point of contact for all backend API interactions.

**Status**: ✅ **COMPLETE**  
**Date Completed**: February 10, 2026  
**Component Location**: `src/services/api.js`

---

## Architecture Overview

### Purpose
The API Service Layer acts as an abstraction between React components and the FastAPI backend. This design pattern provides:
- **Centralized API management** - Single source of truth for all API interactions
- **Consistent error handling** - Standardized error responses across the app
- **Easier testing** - Mock API service in unit tests
- **Easier maintenance** - API changes only need to be updated in one place
- **Request/response logging** - Development debugging capabilities

### Configuration
The API service is configured via environment variables in `.env.local`:

```env
REACT_APP_API_BASE_URL=http://localhost:8000/api
REACT_APP_ENV=development
```

**File**: `.env.local`

---

## Implemented Features

### 1. Axios Instance Configuration ✅
- **Base URL**: Configured from environment variable `REACT_APP_API_BASE_URL`
- **Default Headers**: `Content-Type: application/json`
- **Request Timeout**: 10 seconds
- **Fallback URL**: `http://localhost:8000/api` (development default)

### 2. Student CRUD Methods ✅

#### Create Student - `createStudent(studentData)`
Creates a new student record in the database.

**Parameters:**
```javascript
{
  name: string,      // 2-50 characters, letters/spaces/hyphens/apostrophes
  email: string,     // Valid email format
  roll: string       // 1-20 characters, letters/numbers/hyphens
}
```

**Returns**: Promise<Object> - Created student with auto-generated ID

**Example Usage**:
```javascript
import { createStudent } from '@/services/api';

const newStudent = await createStudent({
  name: 'John Doe',
  email: 'john@example.com',
  roll: 'CS001'
});
console.log(newStudent.id); // MongoDB ObjectId
```

---

#### Fetch All Students - `getStudents()`
Retrieves all students from the database.

**Parameters**: None

**Returns**: Promise<Array> - Array of all student objects

**Example Usage**:
```javascript
import { getStudents } from '@/services/api';

const students = await getStudents();
students.forEach(student => {
  console.log(student.name, student.email);
});
```

---

#### Fetch Single Student - `getStudent(studentId)`
Retrieves a specific student by MongoDB ObjectId.

**Parameters:**
- `studentId` (string) - MongoDB ObjectId

**Returns**: Promise<Object> - Student object with all fields

**Example Usage**:
```javascript
import { getStudent } from '@/services/api';

const student = await getStudent('507f1f77bcf86cd799439011');
console.log(student.name);
```

---

#### Update Student - `updateStudent(studentId, studentData)`
Updates specific fields of an existing student record.

**Parameters:**
- `studentId` (string) - MongoDB ObjectId
- `studentData` (Object) - Fields to update (partial update allowed)
  - `name` (optional)
  - `email` (optional)
  - `roll` (optional)

**Returns**: Promise<Object> - Updated student object

**Example Usage**:
```javascript
import { updateStudent } from '@/services/api';

const updated = await updateStudent('507f1f77bcf86cd799439011', {
  name: 'Jane Doe',
  email: 'jane@example.com'
});
```

---

#### Delete Student - `deleteStudent(studentId)`
Permanently deletes a student record from the database.

**Parameters:**
- `studentId` (string) - MongoDB ObjectId

**Returns**: Promise<boolean> - True on success (HTTP 204 No Content)

**Throws**: AxiosError on failure

**Example Usage**:
```javascript
import { deleteStudent } from '@/services/api';

const success = await deleteStudent('507f1f77bcf86cd799439011');
if (success) {
  console.log('Student deleted successfully');
}
```

---

### 3. Request/Response Interceptors ✅

#### Request Interceptor
- **Logs**: Outgoing requests in development mode
- **Format**: `[API] METHOD URL {data}`
- **Details**: Includes request method, URL, and payload

#### Response Interceptor
- **Success Path**: Logs successful responses in development mode
- **Error Path**: Logs error details including status code and message
- **Format**: `[API] Response {status}`

**Development Logging Example**:
```
[API] POST /students {name: "John", email: "john@example.com", roll: "CS001"}
[API] Response 201: {id: "...", name: "John", ...}
```

---

### 4. Error Handling ✅

#### Error Format
All errors are formatted consistently:

```javascript
{
  status: number,          // HTTP status code (0 if network error)
  message: string,         // User-friendly error message
  detail: string|object,   // Detailed error information from server
  originalError: Error     // Original axios error object
}
```

#### Error Types Handled

**Server Response Errors** (4xx, 5xx):
```javascript
{
  status: 400,
  message: "Bad Request - Please check your input",
  detail: {/* Server response data */}
}
```

**Network Errors**:
```javascript
{
  status: 0,
  message: "No response from server. Please check your connection.",
  detail: "error message"
}
```

**Request Setup Errors**:
```javascript
{
  status: 0,
  message: "error message",
  detail: "error message"
}
```

#### Standard HTTP Status Messages
- **400**: Bad Request - Please check your input
- **404**: Not Found - Resource does not exist
- **409**: Conflict - Resource already exists
- **422**: Validation Error - Please check your input
- **500**: Server Error - Please try again later
- **503**: Service Unavailable - Please try again later

---

### 5. Utility Functions ✅

#### Health Check - `checkApiHealth()`
Verifies that the API server is reachable.

**Returns**: Promise<boolean> - True if API is accessible

**Example Usage**:
```javascript
import { checkApiHealth } from '@/services/api';

const isHealthy = await checkApiHealth();
if (isHealthy) {
  console.log('API is online');
} else {
  console.log('API is offline');
}
```

---

#### Get API Base URL - `getApiBaseUrl()`
Returns the configured API base URL.

**Returns**: string - API base URL

**Example Usage**:
```javascript
import { getApiBaseUrl } from '@/services/api';

console.log(`Using API: ${getApiBaseUrl()}`);
```

---

#### Set Custom Header - `setApiHeader(key, value)`
Adds or updates a custom header for all subsequent requests.

**Parameters:**
- `key` (string) - Header name
- `value` (string) - Header value

**Use Cases**: Adding authentication tokens, API keys, etc.

**Example Usage**:
```javascript
import { setApiHeader } from '@/services/api';

// Add authentication token
setApiHeader('Authorization', `Bearer ${token}`);
```

---

#### Remove Custom Header - `removeApiHeader(key)`
Removes a custom header from all requests.

**Parameters:**
- `key` (string) - Header name to remove

**Example Usage**:
```javascript
import { removeApiHeader } from '@/services/api';

// Remove authentication token on logout
removeApiHeader('Authorization');
```

---

## Usage Patterns

### In React Components

#### Pattern 1: In useEffect (Fetch on Mount)
```javascript
import { useEffect, useState } from 'react';
import { getStudents } from '@/services/api';

function StudentList() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStudents = async () => {
      try {
        const data = await getStudents();
        setStudents(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchStudents();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  return <div>{/* render students */}</div>;
}
```

#### Pattern 2: In Event Handler (Submit)
```javascript
import { createStudent } from '@/services/api';

async function handleSubmit(formData) {
  try {
    const newStudent = await createStudent(formData);
    console.log('Created:', newStudent);
  } catch (error) {
    console.error('Failed:', error.message);
  }
}
```

#### Pattern 3: With Try-Catch Error Handling
```javascript
import { updateStudent } from '@/services/api';

try {
  const updated = await updateStudent(studentId, { name: 'New Name' });
} catch (error) {
  if (error.status === 404) {
    // Student not found
  } else if (error.status === 422) {
    // Validation error
  } else {
    // Other error
  }
}
```

---

## API Response Format

### Successful Response - Create/Read
```javascript
{
  id: "507f1f77bcf86cd799439011",
  name: "John Doe",
  email: "john@example.com",
  roll: "CS001",
  created_at: "2026-02-10T10:30:00Z",
  updated_at: "2026-02-10T10:30:00Z"
}
```

### Successful Response - Array (Get All)
```javascript
[
  { id: "...", name: "John Doe", email: "...", roll: "..." },
  { id: "...", name: "Jane Smith", email: "...", roll: "..." },
  // ...
]
```

### Successful Response - Delete
HTTP 204 No Content (apiClient returns true)

---

## File Structure

```
student-registration/
├── src/
│   ├── services/
│   │   └── api.js              ✅ API Service Layer
│   ├── components/
│   ├── pages/
│   └── ...
├── .env.local                  ✅ Environment Configuration
└── package.json
```

---

## Configuration Reference

### Environment Variables
Location: `.env.local`

| Variable | Default | Description |
|----------|---------|-------------|
| `REACT_APP_API_BASE_URL` | `http://localhost:8000/api` | Backend API endpoint |
| `REACT_APP_ENV` | `development` | Environment mode (affects logging) |

### Axios Configuration
- **Timeout**: 10 seconds (configurable in api.js)
- **Content-Type**: application/json
- **Credentials**: Not included (configure if needed)

---

## Testing the API Service

### Using the API Service Directly
```javascript
// In browser console or test file
import api from '@/services/api';

// Test Create
api.createStudent({
  name: 'Test Student',
  email: 'test@example.com',
  roll: 'TEST001'
}).then(console.log).catch(console.error);

// Test Read All
api.getStudents().then(console.log).catch(console.error);

// Test Health Check
api.checkApiHealth().then(console.log);
```

### Mocking for Unit Tests
```javascript
// In Jest test file
jest.mock('@/services/api', () => ({
  getStudents: jest.fn(() => Promise.resolve([
    { id: '1', name: 'John', email: 'john@example.com', roll: 'CS001' }
  ])),
  createStudent: jest.fn(),
  updateStudent: jest.fn(),
  deleteStudent: jest.fn(),
}));
```

---

## Security Considerations

✅ **Implemented**:
- No sensitive data in API layer
- Consistent error handling (no stack traces exposed)
- HTTPS ready (configure in production)
- Timeout protection (10 seconds)

⚠️ **For Future Enhancement**:
- Add authentication token support (JWT)
- Implement request signing
- Add rate limiting
- Add CSRF protection headers

---

## Performance Notes

- **Timeout**: 10 seconds per request
- **Caching**: Not implemented at API layer (consider React Query in future)
- **Request Size**: No limit imposed at API layer
- **Response Size**: No limit imposed at API layer

---

## Troubleshooting

### "No response from server" Error
- **Cause**: Backend server not running or not accessible
- **Solution**: Start the FastAPI backend: `uvicorn app:app --reload`

### CORS Errors
- **Cause**: API_BASE_URL doesn't match backend CORS configuration
- **Solution**: Update `.env.local` to match backend's ALLOWED_ORIGINS

### Validation Errors (422 Status)
- **Cause**: Invalid data format (email, length, etc.)
- **Solution**: Check field validation in StudentForm component

### 404 Not Found
- **Cause**: Student ID doesn't exist or incorrect endpoint
- **Solution**: Verify student ID and check backend routes

---

## Phase 3.1 Completion Checklist

- ✅ Axios instance created with proper configuration
- ✅ API base URL configured from environment variables
- ✅ All CRUD methods implemented (Create, Read, Update, Delete)
- ✅ Request/Response interceptors added
- ✅ Comprehensive error handling
- ✅ Utility functions (health check, header management)
- ✅ JSDoc comments for all functions
- ✅ Error formatting and standardization
- ✅ Logging for development debugging
- ✅ Default export for import flexibility

---

## Next Steps (Phase 3.2)

The API Service Layer is now ready to be integrated into React components:
- **Phase 3.2**: Implement StudentForm component (uses `createStudent`)
- **Phase 3.3**: Implement StudentList component (uses `getStudents`, `deleteStudent`)
- **Phase 3.4**: Implement EditForm component (uses `getStudent`, `updateStudent`)

---

## Integration Example (Preview for Components)

```javascript
// In StudentForm.js (Phase 3.2)
import { createStudent } from '@/services/api';

// In StudentList.js (Phase 3.3)
import { getStudents, deleteStudent } from '@/services/api';

// In EditForm.js (Phase 3.4)
import { getStudent, updateStudent } from '@/services/api';
```

---

## Additional Resources

- **Backend API Documentation**: See `API_DOCUMENTATION.md`
- **React Migration Plan**: See `REACT_MIGRATION_PLAN.md`
- **Phase 3 Overview**: See root documentation files
- **Axios Documentation**: https://axios-http.com/docs

---

**Implemented by**: AI Assistant  
**Quality Verification**: ✅ Complete API layer with error handling, logging, and documentation
