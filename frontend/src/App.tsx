import { Route, Routes, useNavigate } from "react-router-dom";
import "./index.css";
import DashboardPage from "./pages/DashboardPage";
import ProtectedRoute from "./components/providers/ProtectedRoute";
import { useAuth } from "./hooks/useAuth";
import { useEffect } from "react";
import { useUserStore } from "./store/user";
import AuthPage from "./pages/AuthPage";
import { useShallow } from "zustand/react/shallow";
import EmployeeDetailPage from "./pages/EmployeeDetailPage";

function HomeRedirect() {
  const { loading } = useAuth();
  const navigate = useNavigate();
  const { user } = useUserStore(useShallow((state) => ({ user: state.user })));

  useEffect(() => {
    if (!loading) {
      if (!user) {
        navigate("/auth");
      } else {
        navigate("/dashboard");
      }
    }
  }, [user, loading, navigate]);

  return null;
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomeRedirect />} />
      <Route path="/auth" element={<AuthPage />} />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <DashboardPage />
          </ProtectedRoute>
        }
      />
      {/* Add employee page route */}
      <Route
        path="/me"
        element={
          <ProtectedRoute>
            <div>Employee Page</div>
          </ProtectedRoute>
        }
      />
      <Route
        path="/employee/:id"
        element={
          <ProtectedRoute>
            <EmployeeDetailPage />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}

export default App;
