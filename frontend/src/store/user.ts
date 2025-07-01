import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface User {
  id: string;
  name: string;
  email: string;
  role: "manager" | "employee";
}

type StoreState = {
  user: User | null;
  setUser: (user: User | null) => void;
};

export const useUserStore = create<StoreState>()(
  persist((set) => ({
    user: null,
    setUser: (user: User | null) => set({ user }),
  }),{
    name: "user",
  })
);
