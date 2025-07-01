import { useState } from "react";
import axios from "axios";
import {useUserStore} from "@/store/user";
import { useNavigate } from "react-router-dom";

const API_BASE = import.meta.env.VITE_BACKEND_URL_DEV || "http://localhost:8000";

export function useAuth() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const setUser = useUserStore((state) => state.setUser);
  const navigate = useNavigate();

  const login = async (email: string, password: string) => {
    setLoading(true);
    setError(null);
    try {
      const res = await axios.post(`${API_BASE}/auth/login`, {
        username: email,
        password,
      },{
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

      const { access_token } = res.data;
      localStorage.setItem("token", access_token);
      setUser(res.data.user);
      return {success: true, error: null};
    
    } catch (err: any) {

      setError(err.response?.data?.detail || "Login failed");
      return {success: false, error: err.response?.data?.detail || "Login failed"};
    
    } finally {
      setLoading(false);
    }
  };

  const signup = async ({
    name,
    email,
    password,
    role,
  }: {
    name: string;
    email: string;
    password: string;
    role: "manager" | "employee";
  }) => {
    setLoading(true);
    setError(null);
    try {
      const res = await axios.post(`${API_BASE}/auth/register`, {
        name,
        email,
        password,
        role,
      });
      console.log(res.data);
      
      return {success: true, error: null};
    } catch (err: any) {
      console.log(err);
      setError(err.response?.data?.detail || "Signup failed");
      return {success: false, error: err.response?.data?.detail || "Signup failed"};
    } finally {
      setLoading(false);
    }
  };

  const token = localStorage.getItem("token");

  const fetcher = async (url: string) => {
    try {
      
      const res = await axios.get(`${API_BASE}${url}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      return res.data;
    } catch (err: any) {
      if(err.response.status === 401){
        localStorage.removeItem("token");
        setUser(null);
        navigate("/auth");
      }
      return err.response.data;
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
    navigate("/auth");
  };

  const apiClient = axios.create({
    baseURL: API_BASE,
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return { login, signup, logout, token, fetcher, loading, error, apiClient };
}
