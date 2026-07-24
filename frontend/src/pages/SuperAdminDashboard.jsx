import { useEffect, useState } from "react";

import client from "../api/client";
import DataTable from "../components/DataTable";
import KeyTag from "../components/KeyTag";
import Layout from "../components/Layout";
import StatCard from "../components/StatCard";

export default function SuperAdminDashboard() {
  const [orgs, setOrgs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actioningId, setActioningId] = useState(null);
  const [filter, setFilter] = useState("");

  async function load() {
    setLoading(true);
    const { data } = await client.get("/tenants/organizations/", {
      params: filter ? { status: filter } : {},
    });
    setOrgs(data.results ?? data);
    setLoading(false);
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filter]);

  async function runAction(id, action) {
    setActioningId(id);
    try {
      await client.post(`/tenants/organizations/${id}/${action}/`);
      await load();
    } finally {
      setActioningId(null);
    }
  }

  const pendingCount = orgs.filter((o) => o.status === "PENDING").length;
  const activeCount = orgs.filter((o) => o.status === "ACTIVE").length;

  const filters = [
    { value: "", label: "All" },
    { value: "PENDING", label: "Pending" },
    { value: "ACTIVE", label: "Active" },
    { value: "SUSPENDED", label: "Suspended" },
    { value: "CANCELLED", label: "Cancelled" },
  ];

  return (
    <Layout>
      <div className="mb-6">
        <h1 className="font-display text-2xl font-semibold">Organizations</h1>
        <p className="text-sm text-ink-soft mt-1">Review new hostel businesses and manage existing ones.</p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <StatCard label="Total businesses" value={orgs.length} />
        <StatCard label="Awaiting approval" value={pendingCount} tone="brass" />
        <StatCard label="Active" value={activeCount} tone="moss" />
        <StatCard label="Plans in use" value={new Set(orgs.map((o) => o.subscription_plan)).size} />
      </div>

      <div className="flex gap-2 mb-4 overflow-x-auto pb-1">
        {filters.map((f) => (
          <button
            key={f.value}
            onClick={() => setFilter(f.value)}
            className={`px-3.5 py-1.5 rounded-full text-sm font-medium whitespace-nowrap transition-colors ${
              filter === f.value ? "bg-primary text-white" : "bg-surface border border-border text-ink-soft hover:bg-fog"
            }`}
          >
            {f.label}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="card p-10 text-center text-sm text-ink-soft">Loading organizations…</div>
      ) : (
        <DataTable
          emptyLabel="No organizations match this filter."
          columns={[
            { key: "name", header: "Business" },
            { key: "owner_email", header: "Owner", render: (r) => r.owner_email || "—" },
            { key: "subscription_plan", header: "Plan" },
            {
              key: "status",
              header: "Status",
              render: (r) => <KeyTag status={r.status} />,
            },
            {
              key: "actions",
              header: "Actions",
              className: "space-x-2",
              render: (r) => (
                <div className="flex gap-2">
                  {r.status === "PENDING" && (
                    <>
                      <button
                        disabled={actioningId === r.id}
                        onClick={() => runAction(r.id, "approve")}
                        className="text-xs font-semibold text-moss hover:underline disabled:opacity-50"
                      >
                        Approve
                      </button>
                      <button
                        disabled={actioningId === r.id}
                        onClick={() => runAction(r.id, "reject")}
                        className="text-xs font-semibold text-clay hover:underline disabled:opacity-50"
                      >
                        Reject
                      </button>
                    </>
                  )}
                  {r.status === "ACTIVE" && (
                    <button
                      disabled={actioningId === r.id}
                      onClick={() => runAction(r.id, "suspend")}
                      className="text-xs font-semibold text-clay hover:underline disabled:opacity-50"
                    >
                      Suspend
                    </button>
                  )}
                  {r.status === "SUSPENDED" && (
                    <button
                      disabled={actioningId === r.id}
                      onClick={() => runAction(r.id, "reactivate")}
                      className="text-xs font-semibold text-moss hover:underline disabled:opacity-50"
                    >
                      Reactivate
                    </button>
                  )}
                </div>
              ),
            },
          ]}
          rows={orgs}
        />
      )}
    </Layout>
  );
}
