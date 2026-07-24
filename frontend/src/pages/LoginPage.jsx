import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();

    setError("");
    setSubmitting(true);

    try {
      await login(email, password);

      // Let App.jsx decide which dashboard to show
      navigate("/");
    } catch (err) {
      console.log("========== LOGIN ERROR ==========");
      console.log(err);
      console.log("Response:", err.response);
      console.log("Data:", err.response?.data);
      console.log("Status:", err.response?.status);

      if (err.response) {
        setError(
          JSON.stringify(err.response.data, null, 2)
        );
      } else {
        setError(err.message || "Unknown error");
      }
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen grid md:grid-cols-2">

      {/* Left panel */}
      <div className="hidden md:flex flex-col justify-between bg-primary text-white p-10 lg:p-14">

        <span className="font-display text-2xl font-semibold">
          Nestled
        </span>

        <div>
          <h1 className="font-display text-4xl leading-tight">
            Every bed, every bill, every guest — signed in at one desk.
          </h1>

          <p className="mt-6 text-sm">
            Nestled runs the parts of a hostel that used to live in three
            spreadsheets and a notebook.
          </p>
        </div>

        <p className="text-xs">
          © {new Date().getFullYear()} Nestled
        </p>

      </div>

      {/* Right panel */}
      <div className="flex items-center justify-center p-8">

        <div className="w-full max-w-sm">

          <h1 className="text-2xl font-semibold mb-2">
            Welcome back
          </h1>

          <p className="mb-6 text-gray-500">
            Log in to manage your hostel.
          </p>

          <form onSubmit={handleSubmit} className="space-y-4">

            <div>
              <label>Email</label>

              <input
                className="input w-full"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div>
              <label>Password</label>

              <input
                className="input w-full"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            {error && (
              <pre
                style={{
                  whiteSpace: "pre-wrap",
                  background: "#ffecec",
                  padding: "10px",
                  borderRadius: "8px",
                  color: "red",
                  fontSize: "13px",
                }}
              >
                {error}
              </pre>
            )}

            <button
              type="submit"
              disabled={submitting}
              className="btn-primary w-full"
            >
              {submitting ? "Logging in..." : "Log in"}
            </button>

          </form>

          <p className="mt-6 text-center">
            New hostel business?{" "}
            <Link to="/owner-signup">
              Register it here
            </Link>
          </p>

          <p className="mt-3 text-center">
            Tenant?{" "}
            <Link
              to="/tenant/login"
              className="text-primary font-semibold hover:underline"
            >
              Login here
            </Link>
          </p>

        </div>

      </div>

    </div>
  );
}