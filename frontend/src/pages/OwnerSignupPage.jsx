import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import client from "../api/client";

export default function OwnerSignupPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ organization_name: "", email: "", phone: "", password: "" });
  const [error, setError] = useState("");
  const [done, setDone] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  function update(field) {
    return (e) => setForm((f) => ({ ...f, [field]: e.target.value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      const { data } = await client.post("/auth/owner-signup/", form);
      setDone(data);
    } catch (err) {
      const data = err.response?.data;
      const firstError = data ? Object.values(data).flat()[0] : null;
      setError(firstError || "Something went wrong. Please check your details and try again.");
    } finally {
      setSubmitting(false);
    }
  }

  if (done) {
    return (
      <div className="min-h-screen flex items-center justify-center p-6">
        <div className="card max-w-md w-full p-8 text-center">
          <div className="key-tag key-tag--pending mx-auto mb-4">{done.status}</div>
          <h1 className="font-display text-2xl font-semibold mb-2">You're registered</h1>
          <p className="text-sm text-ink-soft mb-6">{done.detail}</p>
          <Link to="/login" className="btn-primary w-full">Go to login</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-6">
      <div className="card max-w-md w-full p-8">
        <h1 className="font-display text-2xl font-semibold mb-1">Register your hostel business</h1>
        <p className="text-sm text-ink-soft mb-6">
          A Super Admin reviews new businesses before they go live — usually quick.
        </p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="label" htmlFor="organization_name">Business name</label>
            <input
              id="organization_name"
              required
              className="input"
              value={form.organization_name}
              onChange={update("organization_name")}
              placeholder="Sunrise Hostels"
            />
          </div>
          <div>
            <label className="label" htmlFor="email">Your email</label>
            <input
              id="email"
              type="email"
              required
              className="input"
              value={form.email}
              onChange={update("email")}
              placeholder="you@yourhostel.com"
            />
          </div>
          <div>
            <label className="label" htmlFor="phone">Phone (optional)</label>
            <input
              id="phone"
              className="input"
              value={form.phone}
              onChange={update("phone")}
              placeholder="+1 555 0100"
            />
          </div>
          <div>
            <label className="label" htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              required
              minLength={10}
              className="input"
              value={form.password}
              onChange={update("password")}
              placeholder="At least 10 characters"
            />
          </div>

          {error && <p className="text-sm text-clay bg-clay-light rounded-lg px-3 py-2.5">{error}</p>}

          <button type="submit" disabled={submitting} className="btn-primary w-full">
            {submitting ? "Registering…" : "Register business"}
          </button>
        </form>

        <p className="mt-6 text-sm text-ink-soft text-center">
          Already registered?{" "}
          <Link to="/login" className="text-primary font-semibold hover:underline">Log in</Link>
        </p>
      </div>
    </div>
  );
}
