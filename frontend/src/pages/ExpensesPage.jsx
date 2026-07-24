import { Plus } from "lucide-react";
import { useEffect, useState } from "react";

import client from "../api/client";
import DataTable from "../components/DataTable";
import FormDrawer from "../components/FormDrawer";
import Layout from "../components/Layout";
import StatCard from "../components/StatCard";

const CATEGORIES = [
  "ELECTRICITY", "WATER", "INTERNET", "MAINTENANCE", "SALARY",
  "SUPPLIES", "CLEANING", "INSURANCE", "TAXES", "MISCELLANEOUS",
];

const EMPTY_FORM = {
  hostel: "", category: "MISCELLANEOUS", title: "", note: "",
  amount: "", payment_method: "CASH", incurred_on: new Date().toISOString().slice(0, 10),
};

export default function ExpensesPage() {
  const [hostels, setHostels] = useState([]);
  const [expenses, setExpenses] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [form, setForm] = useState(EMPTY_FORM);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [categoryFilter, setCategoryFilter] = useState("");

  const hostelName = (id) => hostels.find((h) => h.id === id)?.name || "—";
  const isMisc = form.category === "MISCELLANEOUS";

  async function load() {
    setLoading(true);
    const params = categoryFilter ? { category: categoryFilter } : {};
    const [hostelsRes, expensesRes, summaryRes] = await Promise.all([
      client.get("/hostels/"),
      client.get("/expenses/", { params }),
      client.get("/expenses/summary/", { params }),
    ]);
    setHostels(hostelsRes.data.results ?? hostelsRes.data);
    setExpenses(expensesRes.data.results ?? expensesRes.data);
    setSummary(summaryRes.data);
    setLoading(false);
  }

  useEffect(() => { load(); }, [categoryFilter]);

  function update(field) {
    return (e) => setForm((f) => ({ ...f, [field]: e.target.value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      await client.post("/expenses/", form);
      setDrawerOpen(false);
      setForm(EMPTY_FORM);
      await load();
    } catch (err) {
      const data = err.response?.data;
      setError(data ? Object.values(data).flat()[0] : "Couldn't save this expense.");
    } finally {
      setSubmitting(false);
    }
  }

  const miscTotal = summary?.by_category?.find((c) => c.category === "MISCELLANEOUS")?.total || 0;

  return (
    <Layout>
      <div className="flex items-center justify-between mb-6 gap-4 flex-wrap">
        <div>
          <h1 className="font-display text-2xl font-semibold">Expenses</h1>
          <p className="text-sm text-ink-soft mt-1">Every outgoing cost, categorized — nothing falls through the cracks.</p>
        </div>
        <button onClick={() => setDrawerOpen(true)} className="btn-primary shrink-0">
          <Plus size={18} /> Log expense
        </button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-6">
        <StatCard label="Total (filtered)" value={`$${Number(summary?.total || 0).toLocaleString()}`} />
        <StatCard label="Entries" value={expenses.length} />
        <StatCard label="Miscellaneous" value={`$${Number(miscTotal).toLocaleString()}`} tone="brass"
          hint="Uncategorized one-offs" />
      </div>

      <div className="flex gap-2 mb-4 overflow-x-auto pb-1">
        <button
          onClick={() => setCategoryFilter("")}
          className={`px-3.5 py-1.5 rounded-full text-sm font-medium whitespace-nowrap transition-colors ${
            categoryFilter === "" ? "bg-primary text-white" : "bg-surface border border-border text-ink-soft hover:bg-fog"
          }`}
        >
          All categories
        </button>
        {CATEGORIES.map((cat) => (
          <button
            key={cat}
            onClick={() => setCategoryFilter(cat)}
            className={`px-3.5 py-1.5 rounded-full text-sm font-medium whitespace-nowrap capitalize transition-colors ${
              categoryFilter === cat ? "bg-primary text-white" : "bg-surface border border-border text-ink-soft hover:bg-fog"
            }`}
          >
            {cat === "MISCELLANEOUS" ? "Miscellaneous" : cat.charAt(0) + cat.slice(1).toLowerCase()}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="card p-10 text-center text-sm text-ink-soft">Loading expenses…</div>
      ) : (
        <DataTable
          emptyLabel="No expenses logged for this filter yet."
          columns={[
            { key: "incurred_on", header: "Date", mono: true },
            { key: "title", header: "Title", render: (r) => (
              <div>
                <div>{r.title}</div>
                {r.category === "MISCELLANEOUS" && r.note && (
                  <div className="text-xs text-ink-soft mt-0.5 max-w-xs whitespace-normal">{r.note}</div>
                )}
              </div>
            ) },
            { key: "hostel", header: "Hostel", render: (r) => hostelName(r.hostel) },
            { key: "category_display", header: "Category" },
            { key: "amount", header: "Amount", mono: true, render: (r) => `$${r.amount}` },
          ]}
          rows={expenses}
        />
      )}

      <FormDrawer open={drawerOpen} title="Log an expense" onClose={() => setDrawerOpen(false)}>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="label">Hostel</label>
            <select required className="input" value={form.hostel} onChange={update("hostel")}>
              <option value="">Select a hostel</option>
              {hostels.map((h) => <option key={h.id} value={h.id}>{h.name}</option>)}
            </select>
          </div>
          <div>
            <label className="label">Category</label>
            <select className="input" value={form.category} onChange={update("category")}>
              {CATEGORIES.map((cat) => (
                <option key={cat} value={cat}>
                  {cat === "MISCELLANEOUS" ? "Miscellaneous" : cat.charAt(0) + cat.slice(1).toLowerCase()}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="label">Title</label>
            <input required className="input" value={form.title} onChange={update("title")}
              placeholder={isMisc ? "e.g. Council inspection fee" : "e.g. March electricity bill"} />
          </div>

          {isMisc && (
            <div>
              <label className="label">What was this for?</label>
              <textarea
                required
                rows={3}
                className="input resize-none"
                value={form.note}
                onChange={update("note")}
                placeholder="Miscellaneous expenses need a short description so future-you (or an auditor) knows what it was."
              />
            </div>
          )}

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="label">Amount</label>
              <input type="number" step="0.01" required className="input" value={form.amount} onChange={update("amount")} />
            </div>
            <div>
              <label className="label">Date incurred</label>
              <input type="date" required className="input" value={form.incurred_on} onChange={update("incurred_on")} />
            </div>
          </div>
          <div>
            <label className="label">Payment method</label>
            <select className="input" value={form.payment_method} onChange={update("payment_method")}>
              <option value="CASH">Cash</option>
              <option value="BANK_TRANSFER">Bank transfer</option>
              <option value="ONLINE">Online payment</option>
              <option value="CARD">Card</option>
              <option value="OTHER">Other</option>
            </select>
          </div>

          {error && <p className="text-sm text-clay bg-clay-light rounded-lg px-3 py-2.5">{error}</p>}

          <button type="submit" disabled={submitting} className="btn-primary w-full">
            {submitting ? "Saving…" : "Save expense"}
          </button>
        </form>
      </FormDrawer>
    </Layout>
  );
}
