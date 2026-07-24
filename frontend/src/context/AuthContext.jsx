import { createContext, useContext, useEffect, useState } from "react";

import client, { clearTokens, setTokens } from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const access = localStorage.getItem("hostel_access");
    if (!access) {
      setLoading(false);
      return;
    }
    client
      .get("/auth/me/")
      .then((res) => setUser(res.data))
      .catch(() => clearTokens())
      .finally(() => setLoading(false));
  }, []);

  async function login(email, password) {
    const { data } = await client.post("/auth/login/", { email, password });
    setTokens({ access: data.access, refresh: data.refresh });
    setUser(data.user);
    return data.user;
  }

  async function logout() {
    const refresh = localStorage.getItem("hostel_refresh");
    try {
      if (refresh) await client.post("/auth/logout/", { refresh });
    } catch {
      // ignore — clear local state regardless
    }
    clearTokens();
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, setUser, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
