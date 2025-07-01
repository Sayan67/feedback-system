// import LoginForm from '@/components/LoginForm'
// import { useUserStore } from '@/store/user';
// import React, { useEffect } from 'react'
// import { useNavigate } from 'react-router-dom';
// import { useShallow } from 'zustand/react/shallow';

// function LoginPage() {
//   const {user} = useUserStore(useShallow((state) => ({ user: state.user })));
//   const navigate = useNavigate();

//   useEffect(() => {
//     if (user) {
//       navigate("/dashboard");
//     }
//   }, [user, navigate]);

//   if (user) {
//     return <div>Loading...</div>;
//   }

//   return (
//     <div className='flex flex-col items-center justify-center h-screen'>
//       <LoginForm />
//     </div>
//   )
// }

// export default LoginPage
