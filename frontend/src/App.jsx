import { Navigate, Route, Routes } from "react-router-dom";

import ProtectedRoute from "./components/ProtectedRoute";
import { useAuth } from "./context/AuthContext";

import ExpensesPage from "./pages/ExpensesPage";
import HostelsPage from "./pages/HostelsPage";
import RoomsPage from "./pages/RoomsPage";
import TenantsPage from "./pages/TenantsPage";
import AllocationsPage from "./pages/AllocationsPage";

import LoginPage from "./pages/LoginPage";
import TenantLoginPage from "./pages/TenantLoginPage";
import OwnerSignupPage from "./pages/OwnerSignupPage";

import OwnerDashboard from "./pages/OwnerDashboard";
import TenantDashboard from "./pages/TenantDashboard";
import SuperAdminDashboard from "./pages/SuperAdminDashboard";

import PaymentsPage from "./pages/PaymentsPage";



function HomeRoute() {

  const { user } = useAuth();


  if (user?.role === "SUPER_ADMIN") {
    return <SuperAdminDashboard />;
  }


  if (user?.role === "TENANT") {
    return <TenantDashboard />;
  }


  return <OwnerDashboard />;

}



export default function App() {


return (

<Routes>


{/* ================= PUBLIC ROUTES ================= */}


<Route
path="/login"
element={<LoginPage />}
/>


<Route
path="/tenant/login"
element={<TenantLoginPage />}
/>


<Route
path="/owner-signup"
element={<OwnerSignupPage />}
/>


<Route
    path="/payments"
    element={
        <ProtectedRoute>
            <PaymentsPage />
        </ProtectedRoute>
    }
/>



{/* ================= DASHBOARD ================= */}


<Route

path="/"

element={

<ProtectedRoute>

<HomeRoute />

</ProtectedRoute>

}

/>



{/* ================= HOSTELS ================= */}


<Route

path="/hostels"

element={

<ProtectedRoute allowedRoles={[
"HOSTEL_OWNER",
"HOSTEL_MANAGER"
]}>

<HostelsPage />

</ProtectedRoute>

}

/>



{/* ================= ROOMS & BEDS ================= */}


<Route

path="/rooms"

element={

<ProtectedRoute allowedRoles={[
"HOSTEL_OWNER",
"HOSTEL_MANAGER"
]}>

<RoomsPage />

</ProtectedRoute>

}

/>



{/* ================= TENANTS ================= */}


<Route

path="/tenants"

element={

<ProtectedRoute allowedRoles={[
"HOSTEL_OWNER",
"HOSTEL_MANAGER"
]}>

<TenantsPage />

</ProtectedRoute>

}

/>



{/* ================= BED ALLOCATIONS ================= */}


<Route

path="/allocations"

element={

<ProtectedRoute allowedRoles={[
"HOSTEL_OWNER",
"HOSTEL_MANAGER"
]}>

<AllocationsPage />

</ProtectedRoute>

}

/>



{/* ================= EXPENSES ================= */}


<Route

path="/expenses"

element={

<ProtectedRoute allowedRoles={[
"HOSTEL_OWNER",
"HOSTEL_MANAGER"
]}>

<ExpensesPage />

</ProtectedRoute>

}

/>



{/* ================= FALLBACK ================= */}


<Route

path="*"

element={

<Navigate to="/" replace />

}

/>


</Routes>

);


}