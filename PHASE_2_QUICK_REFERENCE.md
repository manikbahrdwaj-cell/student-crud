# Phase 2: Quick Reference Guide

## 🚀 Getting Started

### Start Development Server
```bash
cd student-registration
npm start
```
Opens at: `http://localhost:3000`

---

## 📁 Project Structure

```
src/
├── components/
│   ├── StudentForm.js      - Reusable form (create/edit)
│   ├── StudentList.js      - Student table display
│   └── EditForm.js         - Edit wrapper component
├── pages/
│   ├── Dashboard.js        - Main page (localhost:3000/dashboard)
│   ├── CreatePage.js       - Create student (localhost:3000/create)
│   └── EditPage.js         - Edit student (localhost:3000/edit/:id)
├── services/
│   └── api.js              - All API methods
├── App.js                  - Routing setup
└── index.css               - Tailwind CSS
```

---

## 🔧 Configuration

### Environment Variables (.env.local)
```
REACT_APP_API_BASE_URL=http://localhost:8000/api
```

### Tailwind Config
- `tailwind.config.js` - Theme customization
- `postcss.config.js` - PostCSS plugins

---

## 📡 API Methods (services/api.js)

```javascript
import { studentAPI } from './services/api';

// Create student
await studentAPI.createStudent({ name, email, roll });

// Get all students
await studentAPI.getStudents();

// Get single student
await studentAPI.getStudent(id);

// Update student
await studentAPI.updateStudent(id, { name, email, roll });

// Delete student
await studentAPI.deleteStudent(id);
```

---

## 🧩 Component Usage

### StudentForm (Create/Edit)
```javascript
<StudentForm 
  onSubmitSuccess={handleSuccess}
  initialData={studentData}     // For edit mode
  isEdit={true}                 // Toggle edit mode
/>
```

### StudentList
```javascript
<StudentList />
```

---

## 🛣️ Routes

| Path | Component | Purpose |
|------|-----------|---------|
| `/` | Redirect to /dashboard | Auto-forward |
| `/dashboard` | Dashboard | View all students |
| `/create` | CreatePage | Create new student |
| `/edit/:id` | EditPage | Edit student |

---

## 🎨 Tailwind CSS Classes Used

### Form Elements
```
input: px-4 py-2 border rounded-lg focus:ring-2
button: px-4 py-2 bg-color text-white rounded-lg hover:bg-dark
```

### Table
```
table: w-full border-collapse
tr: border-b hover:bg-gray-100
td: px-6 py-4
```

### Alerts
```
error: bg-red-100 border-red-400 text-red-700
success: bg-green-100 border-green-400 text-green-700
```

---

## 🔌 Frontend-Backend Connection

**Frontend**: React at `http://localhost:3000`  
**Backend**: FastAPI at `http://localhost:8000`  
**API Base**: `http://localhost:8000/api`

### Required Backend Endpoints
```
POST   /api/students           - Create
GET    /api/students           - List all
GET    /api/students/{id}      - Get one
PUT    /api/students/{id}      - Update
DELETE /api/students/{id}      - Delete
```

### CORS Required
Backend must enable CORS for `http://localhost:3000`

---

## 📦 Installed Dependencies

```json
{
  "react": "^19.2.4",
  "react-dom": "^19.2.4",
  "react-router-dom": "^7.13.0",
  "axios": "^1.13.5",
  "tailwindcss": "^4.1.18",
  "postcss": "^8.5.6",
  "autoprefixer": "^10.4.24",
  "react-icons": "^5.5.0"
}
```

---

## 🧪 Testing the Frontend

1. Start backend: `python api.py`
2. Start frontend: `npm start`
3. Navigate to `http://localhost:3000`
4. Use Create button to add student
5. View list of students
6. Click Edit to modify
7. Click Delete to remove

---

## 📝 Form Validation

**Name**: Required, non-empty  
**Email**: Required, valid format (user@example.com)  
**Roll**: Required, non-empty

---

## 🔄 Error Handling

- ✅ Network errors show user-friendly messages
- ✅ Form validation prevents invalid submissions
- ✅ Delete confirmation prevents accidental deletion
- ✅ Loading states prevent double-submission

---

## 🎯 Next Phase (Phase 3)

Phase 3 will add:
- Audio recording components
- Enhanced validation
- Styling refinements
- Testing coverage

---

## ⚡ Quick Commands

```bash
# Start development
npm start

# Build for production
npm run build

# Run tests
npm test
```

---

**Phase 2 Status**: ✅ Complete and Ready for Testing
