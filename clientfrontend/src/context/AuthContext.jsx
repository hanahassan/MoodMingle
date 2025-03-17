// // src/context/AuthContext.jsx
// import React, { createContext, useState, useContext, useEffect } from 'react';

// const AuthContext = createContext(null);

// // Initial dummy users for testing
// const initialDummyUsers = [
//   {
//     id: "user1",
//     username: "testuser",
//     email: "user@example.com",
//     password: "password123",
//     displayName: "Test User",
//     location: "New York, USA",
//     interests: ["Outdoor Adventures", "Sports"],
//     memberSince: "February 2024"
//   },
//   {
//     id: "mariam",
//     username: "mariam",
//     email: "mariam@example.com",
//     password: "password12",
//     displayName: "Mariam Ibrahim",
//     location: "Calgary, CA",
//     interests: ["Horror Movies", "Reading"],
//     memberSince: "March 2024"
//   }
// ];

// export const AuthProvider = ({ children }) => {
//   // Load users from localStorage or use initial dummy users
//   const [users, setUsers] = useState(() => {
//     const savedUsers = localStorage.getItem('moodmingle_users');
//     return savedUsers ? JSON.parse(savedUsers) : initialDummyUsers;
//   });
  
//   const [isLoggedIn, setIsLoggedIn] = useState(false);
//   const [user, setUser] = useState(null);
  
//   // Save users to localStorage whenever they change
//   useEffect(() => {
//     // Store the full users array in localStorage
//     localStorage.setItem('moodmingle_users', JSON.stringify(users));
//     console.log('Users saved to localStorage:', users);
//   }, [users]);
  
//   // Check for saved user session on initial load
//   useEffect(() => {
//     const savedUser = localStorage.getItem('moodmingle_user');
//     if (savedUser) {
//       const parsedUser = JSON.parse(savedUser);
//       setUser(parsedUser);
//       setIsLoggedIn(true);
//     }
//   }, []);

//   const login = (credentials) => {
//     console.log('Attempting login with:', credentials);
//     console.log('Available users:', users);
    
//     // Find user by email or username
//     const foundUser = users.find(u => 
//       (u.email === credentials.email || u.username === credentials.username) && 
//       u.password === credentials.password
//     );
    
//     if (foundUser) {
//       // Create a copy without the password for security
//       const { password, ...safeUserData } = foundUser;
      
//       // Store in state
//       setUser(safeUserData);
//       setIsLoggedIn(true);
      
//       // Save to localStorage for session persistence
//       localStorage.setItem('moodmingle_user', JSON.stringify(safeUserData));
      
//       return { success: true, user: safeUserData };
//     } else {
//       return { success: false, error: "Invalid username/email or password" };
//     }
//   };

//   const signup = (userData) => {
//     // Check if username or email already exists
//     const usernameExists = users.some(u => u.username === userData.username);
//     if (usernameExists) {
//       return { success: false, error: "Username already taken" };
//     }
    
//     const emailExists = users.some(u => u.email === userData.email);
//     if (emailExists) {
//       return { success: false, error: "Email already registered" };
//     }
    
//     // Get current date for memberSince
//     const currentDate = new Date();
//     const month = currentDate.toLocaleString('default', { month: 'long' });
//     const year = currentDate.getFullYear();
    
//     // Create new user
//     const newUser = {
//       id: `user_${Date.now()}`, // Generate unique ID
//       username: userData.username,
//       email: userData.email,
//       password: userData.password, // In a real app, this would be hashed
//       displayName: userData.displayName || userData.username,
//       location: userData.location || "",
//       interests: [],
//       memberSince: `${month} ${year}`
//     };
    
//     // Add to users array
//     const updatedUsers = [...users, newUser];
//     setUsers(updatedUsers);
    
//     console.log('New user created:', newUser);
//     console.log('Updated users array:', updatedUsers);
    
//     // Auto-login the new user
//     const { password, ...safeUserData } = newUser;
//     setUser(safeUserData);
//     setIsLoggedIn(true);
//     localStorage.setItem('moodmingle_user', JSON.stringify(safeUserData));
    
//     return { success: true, user: safeUserData };
//   };

//   const logout = () => {
//     // Reset user state
//     setIsLoggedIn(false);
//     setUser(null);
    
//     // Clear user session data
//     localStorage.removeItem('moodmingle_user');
//     localStorage.removeItem('previousInterests');
    
//     // Reset any other stored user data
//     localStorage.removeItem('savedActivities');
    
//     // Also clear any user-specific saved activities
//     Object.keys(localStorage).forEach(key => {
//       if (key.startsWith('savedActivities_')) {
//         localStorage.removeItem(key);
//       }
//     });
    
//     // IMPORTANT: Do NOT clear the users array or localStorage entry
//     // We need to keep the users data for future logins
    
//     // Force a page refresh to ensure all components reset
//     window.location.href = '/';
//   };

//   const updateUserInterests = (interests) => {
//     if (user) {
//       // Update user in state
//       const updatedUser = {
//         ...user,
//         interests: interests
//       };
//       setUser(updatedUser);
      
//       // Update user in users array
//       const updatedUsers = users.map(u => 
//         u.id === user.id ? { ...u, interests: interests } : u
//       );
//       setUsers(updatedUsers);
      
//       // Save to localStorage
//       localStorage.setItem('moodmingle_user', JSON.stringify(updatedUser));
      
//       // In a real app, you would also make an API call to update the database
//       console.log('Updating user interests in database:', interests);
//     }
//   };

//   const updateUserProfile = (profileData) => {
//     if (user) {
//       // Update user in state
//       const updatedUser = {
//         ...user,
//         ...profileData
//       };
//       setUser(updatedUser);
      
//       // Update user in users array
//       const updatedUsers = users.map(u => 
//         u.id === user.id ? { ...u, ...profileData, password: u.password } : u
//       );
//       setUsers(updatedUsers);
      
//       // Save to localStorage
//       localStorage.setItem('moodmingle_user', JSON.stringify(updatedUser));
      
//       // In a real app, you would also make an API call to update the database
//       console.log('Updating user profile in database:', profileData);
      
//       return { success: true };
//     }
//     return { success: false, error: "User not logged in" };
//   };

//   return (
//     <AuthContext.Provider 
//       value={{ 
//         isLoggedIn, 
//         user, 
//         login,
//         signup,
//         logout,
//         updateUserInterests,
//         updateUserProfile,
//         users // Export all users for admin purposes
//       }}
//     >
//       {children}
//     </AuthContext.Provider>
//   );
// };

// export const useAuth = () => useContext(AuthContext);



// src/context/AuthContext.jsx
// src/context/AuthContext.jsx
import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext(null);

// API base URL - Change this to match your Flask server address
const API_BASE_URL = 'http://localhost:5001';

export const AuthProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Check if user is already logged in when the app loads
  useEffect(() => {
    const fetchUser = async () => {
      try {
        setIsLoading(true);
        const response = await axios.get(`${API_BASE_URL}/current-user`, {
          withCredentials: true, // Important for session cookies
        });

        console.log('Current user response:', response.data);

        const fetchedUser = response.data.user;

        if (fetchedUser && !fetchedUser.isGuest) {
          // If there is a logged-in user, set the user and mark them as logged in
          setUser(fetchedUser);
          setIsLoggedIn(true);
        } else {
          // If the user is a guest or none exists, ensure logged out state
          setUser(null);
          setIsLoggedIn(false);
        }
      } catch (error) {
        console.error('Error fetching user session', error);
        setUser(null);
        setIsLoggedIn(false);
      } finally {
        setIsLoading(false);
      }
    };

    fetchUser();
  }, []);

  const login = async (credentials) => {
    try {
      console.log('Attempting login with:', credentials);
      
      const response = await axios.post(`${API_BASE_URL}/login`, {
        username: credentials.emailOrUsername, // Send as username to match backend
        password: credentials.password
      }, {
        withCredentials: true, // Important for session cookies
      });

      console.log('Login response:', response.data);

      if (response.data.success) {
        setUser(response.data.user);
        setIsLoggedIn(true);
        return { success: true, user: response.data.user };
      } else {
        return { success: false, error: response.data.error || "Login failed" };
      }
    } catch (error) {
      console.error('Login failed:', error);
      console.error('Error response:', error.response?.data);
      return { 
        success: false, 
        error: error.response?.data?.error || "An error occurred during login" 
      };
    }
  };

  const signup = async (userData) => {
    try {
      console.log('Attempting signup with:', userData);
      
      const response = await axios.post(`${API_BASE_URL}/signup`, {
        username: userData.username,
        email: userData.email,
        password: userData.password,
        displayName: userData.displayName
      }, {
        withCredentials: true,
      });

      console.log('Signup response:', response.data);
      
      if (response.data.success) {
        // Auto-login after successful signup
        setUser(response.data.user);
        setIsLoggedIn(true);
        return { success: true, user: response.data.user };
      } else {
        return { success: false, error: response.data.error || "Signup failed" };
      }
    } catch (error) {
      console.error('Signup failed:', error);
      console.error('Error response:', error.response?.data);
      return { 
        success: false, 
        error: error.response?.data?.error || "An error occurred during signup" 
      };
    }
  };

  const logout = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/logout`, {}, { 
        withCredentials: true 
      });
      
      console.log('Logout response:', response.data);
      
      setUser(null);
      setIsLoggedIn(false);
      // Reset state or perform a page refresh
      window.location.href = '/';
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  const updateUserInterests = async (interests) => {
    if (user) {
      try {
        console.log('Updating interests:', interests);
        
        const response = await axios.put(`${API_BASE_URL}/user/interests`, { 
          username: user.username,
          interests 
        }, {
          withCredentials: true
        });
        
        console.log('Update interests response:', response.data);
        
        if (response.data.success) {
          setUser((prevUser) => ({ ...prevUser, interests }));
          return { success: true };
        }
        return { success: false, error: response.data.error };
      } catch (error) {
        console.error('Error updating interests', error);
        console.error('Error response:', error.response?.data);
        return { success: false, error: "Failed to update interests" };
      }
    }
    return { success: false, error: "User not logged in" };
  };

  const updateUserProfile = async (profileData) => {
    if (user) {
      try {
        console.log('Updating profile:', profileData);
        
        const response = await axios.put(`${API_BASE_URL}/update-profile`, {
          username: user.username,
          ...profileData
        }, {
          withCredentials: true
        });
        
        console.log('Update profile response:', response.data);
        
        if (response.data.success) {
          setUser((prevUser) => ({ ...prevUser, ...profileData }));
          return { success: true };
        }
        return { success: false, error: response.data.error };
      } catch (error) {
        console.error('Error updating profile', error);
        console.error('Error response:', error.response?.data);
        return { success: false, error: "Failed to update profile" };
      }
    }
    return { success: false, error: "User not logged in" };
  };

  // Testing function to execute SQL - ONLY FOR DEVELOPMENT
  const executeSql = async (query) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/execute-sql`, { query });
      return response.data;
    } catch (error) {
      console.error('Error executing SQL:', error);
      return { success: false, error: error.response?.data?.error || "SQL execution failed" };
    }
  };

  return (
    <AuthContext.Provider
      value={{
        isLoggedIn,
        user,
        login,
        signup,
        logout,
        updateUserInterests,
        updateUserProfile,
        isLoading,
        executeSql // Only include in development mode
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);