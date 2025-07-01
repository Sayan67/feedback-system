import { Navigate } from "react-router-dom";
import useSWR from "swr";
import type { JSX } from "react";
import { useAuth } from "@/hooks/useAuth";


export default function ProtectedRoute({ children }: { children: JSX.Element }) {
    const { fetcher } = useAuth();
  const { data, error } = useSWR("/auth/me", fetcher);
  
  if (error) return <Navigate to="/" />;
  if (!data) return <div>Loading...</div>;

  return children;
}
