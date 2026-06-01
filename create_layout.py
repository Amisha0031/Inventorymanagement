import os

pages_dir = "frontend/src/pages"
layout_dir = "frontend/src/components/layout"
os.makedirs(pages_dir, exist_ok=True)
os.makedirs(layout_dir, exist_ok=True)

app_tsx = """import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Layout from './components/layout/Layout';
import Dashboard from './pages/Dashboard';
import Products from './pages/Products';
import Customers from './pages/Customers';
import Orders from './pages/Orders';
import Login from './pages/Login';

const queryClient = new QueryClient();

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const token = localStorage.getItem('token');
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return <>{children}</>;
};

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<ProtectedRoute><Layout /></ProtectedRoute>}>
            <Route index element={<Dashboard />} />
            <Route path="products" element={<Products />} />
            <Route path="customers" element={<Customers />} />
            <Route path="orders" element={<Orders />} />
          </Route>
        </Routes>
      </Router>
    </QueryClientProvider>
  );
}
export default App;
"""

layout_tsx = """import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Navbar from './Navbar';

const Layout = () => {
  return (
    <div className="flex h-screen bg-muted/20">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Navbar />
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-muted/10 p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
};
export default Layout;
"""

sidebar_tsx = """import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Package, Users, ShoppingCart, LogOut } from 'lucide-react';
import { cn } from '../../lib/utils';

const navigation = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'Products', href: '/products', icon: Package },
  { name: 'Customers', href: '/customers', icon: Users },
  { name: 'Orders', href: '/orders', icon: ShoppingCart },
];

const Sidebar = () => {
  return (
    <div className="flex h-full w-64 flex-col border-r bg-card">
      <div className="flex h-16 items-center px-6 border-b">
        <h2 className="text-lg font-bold tracking-tight">IOMS Dashboard</h2>
      </div>
      <div className="flex-1 overflow-y-auto py-4">
        <nav className="space-y-1 px-4">
          {navigation.map((item) => (
            <NavLink
              key={item.name}
              to={item.href}
              className={({ isActive }) =>
                cn(
                  isActive
                    ? 'bg-primary/10 text-primary'
                    : 'text-muted-foreground hover:bg-muted hover:text-foreground',
                  'group flex items-center rounded-md px-3 py-2 text-sm font-medium'
                )
              }
            >
              <item.icon className="mr-3 h-5 w-5 flex-shrink-0" aria-hidden="true" />
              {item.name}
            </NavLink>
          ))}
        </nav>
      </div>
      <div className="border-t p-4">
        <button
          onClick={() => {
            localStorage.removeItem('token');
            window.location.href = '/login';
          }}
          className="flex w-full items-center rounded-md px-3 py-2 text-sm font-medium text-muted-foreground hover:bg-muted hover:text-foreground"
        >
          <LogOut className="mr-3 h-5 w-5 flex-shrink-0" />
          Logout
        </button>
      </div>
    </div>
  );
};
export default Sidebar;
"""

navbar_tsx = """import { Bell } from 'lucide-react';

const Navbar = () => {
  return (
    <header className="flex h-16 items-center justify-between border-b bg-card px-6">
      <div className="flex-1" />
      <div className="flex items-center gap-4">
        <button className="rounded-full p-2 text-muted-foreground hover:bg-muted">
          <Bell className="h-5 w-5" />
        </button>
        <div className="h-8 w-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground font-bold">
          AD
        </div>
      </div>
    </header>
  );
};
export default Navbar;
"""

with open("frontend/src/App.tsx", "w") as f: f.write(app_tsx)
with open(os.path.join(layout_dir, "Layout.tsx"), "w") as f: f.write(layout_tsx)
with open(os.path.join(layout_dir, "Sidebar.tsx"), "w") as f: f.write(sidebar_tsx)
with open(os.path.join(layout_dir, "Navbar.tsx"), "w") as f: f.write(navbar_tsx)

print("Layout created.")
