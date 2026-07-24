import { Plus } from "lucide-react";
import { useEffect, useState } from "react";

import client from "../api/client";
import DataTable from "../components/DataTable";
import FormDrawer from "../components/FormDrawer";
import Layout from "../components/Layout";

const EMPTY_FORM = {
  name: "", address: "", city: "", country: "",
  registration_number: "", license_number: "", contact_phone: "", contact_email: "",
};

export default function HostelsPage() {
  const [hostels, setHostels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [form, setForm] = useState(EMPTY_FORM);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function load() {
    setLoading(true);
    const { data } = await client.get("/hostels/");
    setHostels(data.results ?? data);
    setLoading(false);
  }

  useEffect(() => { load(); }, []);

  function update(field) {
    return (e) => setForm((f) => ({ ...f, [field]: e.target.value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      await client.post("/hostels/", form);
      setDrawerOpen(false);
      setForm(EMPTY_FORM);
      await load();
    } catch (err) {
      const data = err.response?.data;
      setError(data ? Object.values(data).flat()[0] : "Couldn't save this hostel. Check the details and try again.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <Layout>
      <div className="flex items-center justify-between mb-6 gap-4">
        <div>
          <h1 className="font-display text-2xl font-semibold">Hostels</h1>
          <p className="text-sm text-ink-soft mt-1">The physical locations your business operates.</p>
        </div>
        <button onClick={() => setDrawerOpen(true)} className="btn-primary shrink-0">
          <Plus size={18} /> Add hostel
        </button>
      </div>

      {loading ? (
        <div className="card p-10 text-center text-sm text-ink-soft">Loading hostels…</div>
      ) : (
        <DataTable
          emptyLabel="No hostels yet. Add your first location to get started."
          columns={[
            { key: "name", header: "Name" },
            { key: "city", header: "City" },
            { key: "country", header: "Country" },
            { key: "contact_phone", header: "Phone", render: (r) => r.contact_phone || "—" },
            { key: "registration_number", header: "Registration #", mono: true, render: (r) => r.registration_number || "—" },
          ]}
          rows={hostels}
        />
      )}

      <FormDrawer open={drawerOpen} title="Add a hostel" onClose={() => setDrawerOpen(false)}>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="label">Name</label>
            <input required className="input" value={form.name} onChange={update("name")} placeholder="Sunrise Downtown" />
          </div>
          <div>
            <label className="label">Address</label>
            <input required className="input" value={form.address} onChange={update("address")} placeholder="1 Main St" />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="label">City</label>
              <input required className="input" value={form.city} onChange={update("city")} />
            </div>
            <div>
              <label className="label">Country</label>
              <input required className="input" value={form.country} onChange={update("country")} />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="label">Registration #</label>
              <input className="input" value={form.registration_number} onChange={update("registration_number")} />
            </div>
            <div>
              <label className="label">License #</label>
              <input className="input" value={form.license_number} onChange={update("license_number")} />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="label">Contact phone</label>
              <input className="input" value={form.contact_phone} onChange={update("contact_phone")} />
            </div>
            <div>
              <label className="label">Contact email</label>
              <input type="email" className="input" value={form.contact_email} onChange={update("contact_email")} />
            </div>
          </div>

          {error && <p className="text-sm text-clay bg-clay-light rounded-lg px-3 py-2.5">{error}</p>}

          <button type="submit" disabled={submitting} className="btn-primary w-full">
            {submitting ? "Saving…" : "Save hostel"}
          </button>
        </form>
      </FormDrawer>
    </Layout>
  );
}
