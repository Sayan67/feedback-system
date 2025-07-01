// src/pages/AuthPage.tsx
import { useEffect, useState } from 'react';
import LoginForm from '@/components/LoginForm';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import SignupForm from '@/components/SignupForm';
import { useNavigate } from 'react-router-dom';
import { useUserStore } from '@/store/user';
import { useShallow } from 'zustand/react/shallow';

export default function AuthPage() {
  const [tab, setTab] = useState('login');
  const navigate = useNavigate();
  const {user} = useUserStore(useShallow((state) => ({ user: state.user })));

  useEffect(() => {
    if (user) {
      navigate("/dashboard");
    }
  }, [user, navigate]);

  if (user) {
    return <div>Loading...</div>;
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="w-full max-w-md space-y-6">
        <Tabs value={tab} onValueChange={setTab} className="w-full">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="login">Login</TabsTrigger>
            <TabsTrigger value="signup">Sign Up</TabsTrigger>
          </TabsList>
          <TabsContent value="login">
            <LoginForm />
          </TabsContent>
          <TabsContent value="signup">
            <SignupForm />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
