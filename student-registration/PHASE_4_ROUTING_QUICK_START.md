# Phase 4: Routing Setup - Quick Reference

## 🚀 Quick Start

### 1. Using Routes in Components
```javascript
import { ROUTES } from '../routes';

// Use in Link or useNavigate
<Link to={ROUTES.DASHBOARD}>Dashboard</Link>
```

### 2. Route Constants Available
```javascript
ROUTES.HOME                    // '/'
ROUTES.DASHBOARD               // '/dashboard'
ROUTES.CREATE                  // '/create'
ROUTES.EDIT                    // '/edit/:id'
ROUTES.NOT_FOUND               // '*'
```

### 3. Navigation Items
```javascript
import { NAVIGATION_ITEMS } from '../routes';

// Use in loops to generate nav links
NAVIGATION_ITEMS.map(item => ({
  label: item.label,
  path: item.path,
  icon: item.icon
}))
// Returns: Dashboard, Add Student links with icons
```

### 4. Route Metadata
```javascript
import { getRouteTitle, getRouteDescription } from '../routes';

getRouteTitle(ROUTES.DASHBOARD)        // 'Dashboard'
getRouteDescription(ROUTES.CREATE)     // 'Add a new student to the system'
isPublicRoute(ROUTES.DASHBOARD)        // true
```

## 📁 Key Files

| File | Purpose |
|------|---------|
| `src/routes/index.js` | Route configuration & constants |
| `src/components/MainLayout.js` | Main layout wrapper |
| `src/components/ProtectedRoute.js` | Protected route wrapper |
| `src/pages/NotFound.js` | 404 error page |
| `src/App.js` | Main app with routing |

## 🎯 Common Tasks

### Add a New Route

1. **Add to ROUTES constants** (`src/routes/index.js`):
```javascript
export const ROUTES = {
  DASHBOARD: '/dashboard',
  CREATE: '/create',
  NEW_FEATURE: '/new-feature',  // ← Add here
};
```

2. **Add to NAVIGATION_ITEMS** (if it should appear in menu):
```javascript
export const NAVIGATION_ITEMS = [
  { label: 'Dashboard', path: ROUTES.DASHBOARD, icon: 'FiHome' },
  { label: 'New Feature', path: ROUTES.NEW_FEATURE, icon: 'FiStar' },  // ← Add here
];
```

3. **Add to ROUTE_META** (for metadata):
```javascript
export const ROUTE_META = {
  [ROUTES.NEW_FEATURE]: {
    title: 'New Feature',
    description: 'Feature description',
    publicRoute: true,
  },
};
```

4. **Add route in App.js**:
```javascript
<Route
  path={ROUTES.NEW_FEATURE}
  element={
    <MainLayout>
      <NewFeaturePage />
    </MainLayout>
  }
/>
```

### Create Protected Route (for Auth)

```javascript
<Route
  path={ROUTES.ADMIN}
  element={
    <ProtectedRoute isAuthenticated={user.isAdmin}>
      <MainLayout>
        <AdminPage />
      </MainLayout>
    </ProtectedRoute>
  }
/>
```

### Add New Navigation Item Icon

1. Import icon in `Navigation.js`:
```javascript
import { FiHome, FiPlus, FiSettings } from 'react-icons/fi';
```

2. Add to icon map:
```javascript
const getIcon = (iconName) => {
  const iconMap = {
    FiHome: <FiHome size={18} />,
    FiPlus: <FiPlus size={18} />,
    FiSettings: <FiSettings size={18} />,  // ← Add here
  };
};
```

3. Update NAVIGATION_ITEMS:
```javascript
icon: 'FiSettings'  // Must match the key in iconMap
```

## 🧪 Testing Routes

### 1. Test Navigation
- Click Dashboard → `/dashboard`
- Click Add Student → `/create`
- Click Edit on a student → `/edit/:id`

### 2. Test 404 Page
- Navigate to invalid URL: `http://localhost:3000/invalid`
- Should see 404 page with back button

### 3. Test Route Constants
- Open DevTools Console
- Run: `import { ROUTES } from './src/routes'; console.log(ROUTES);`
- Should see all route constants

## 🔗 Route Navigation Examples

```javascript
// Using Link
import { Link } from 'react-router-dom';
import { ROUTES } from '../routes';

<Link to={ROUTES.DASHBOARD}>Go to Dashboard</Link>

// Using useNavigate hook
import { useNavigate } from 'react-router-dom';

const navigate = useNavigate();
navigate(ROUTES.CREATE);

// Using useLocation to check current route
import { useLocation } from 'react-router-dom';

const location = useLocation();
if (location.pathname === ROUTES.DASHBOARD) {
  // On dashboard
}

// Using useParams to get route parameters
import { useParams } from 'react-router-dom';

const { id } = useParams();
// From /edit/:id route
```

## 🎨 MainLayout Usage

```javascript
// Automatically includes:
// - Navigation header
// - Main content area
// - Toast notifications

<MainLayout>
  <YourPageComponent />
</MainLayout>

// Your component gets wrapped in full layout
```

## 📝 Complete Navigation Example

```javascript
import { NAVIGATION_ITEMS } from '../routes';

function Navigation() {
  return (
    <nav>
      {NAVIGATION_ITEMS.map(item => (
        <Link key={item.path} to={item.path}>
          {item.label}
        </Link>
      ))}
    </nav>
  );
}
```

## ⚡ Best Practices

1. **Always use ROUTES constants** - Never hardcode paths
2. **Use MainLayout consistently** - For uniform look & feel
3. **Add metadata for new routes** - Help with future features
4. **Test 404 handling** - Ensure fallback works
5. **Use useNavigate for actions** - For programmatic navigation
6. **Use Link for UI navigation** - For better performance

## 🚫 Common Mistakes

❌ `<Link to="/dashboard">` → ✅ `<Link to={ROUTES.DASHBOARD}>`

❌ Hardcoded URLs everywhere → ✅ Use ROUTES constants

❌ Forgetting MainLayout wrapper → ✅ Always wrap with MainLayout

❌ Not adding to NAVIGATION_ITEMS → ✅ Add so it appears in menu

---

**For full documentation**: See `PHASE_4_ROUTING_ENHANCEMENT.md`
