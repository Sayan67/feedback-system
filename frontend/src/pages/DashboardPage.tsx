import { Button } from "@/components/ui/button";
import { useAuth } from "@/hooks/useAuth";
import { useUserStore } from "@/store/user";
import { useShallow } from "zustand/react/shallow";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ManagerDashboard from "@/components/dashboard/ManagerDashboard";
import EmployeeDashboard from "@/components/dashboard/EmployeeDashboard";

function DashboardPage() {
  const { logout } = useAuth();
  const { user } = useUserStore(useShallow((state) => ({ user: state.user })));
  const navigate = useNavigate();

  useEffect(() => {
    if (!user) {
      navigate("/auth");
    }
  }, [user, navigate]);

  if (!user) {
    return <div>Loading...</div>;
  }

  return (
    <div className="flex flex-col items-center h-screen w-full ga">
      {user?.role === "manager" ? (
        <ManagerDashboard />
      ) : (
        <EmployeeDashboard />
      )}
      <div className="absolute bottom-4">
        <Button variant={"destructive"} onClick={logout}>
          Logout
        </Button>
      </div>
    </div>
  );
}

export default DashboardPage;
