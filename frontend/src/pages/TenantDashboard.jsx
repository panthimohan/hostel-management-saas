import { useEffect, useState } from "react";

import client from "../api/client";
import Layout from "../components/Layout";

export default function TenantDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    client.get("/beds/my-room/").then((res) => {
      setData(res.data);
      setLoading(false);
    });
  }, []);

  return (
    <Layout>
      <div className="mb-6">
        <h1 className="font-display text-2xl font-semibold">My room</h1>
        <p className="text-sm text-ink-soft mt-1">Where you're staying and what it costs.</p>
      </div>

      {loading ? (
        <div className="card p-10 text-center text-sm text-ink-soft">Loading…</div>
      ) : data?.current ? (
        <div className="card p-6 sm:p-8 max-w-lg">
          <p className="text-xs font-semibold uppercase tracking-wide text-ink-soft mb-1">
            {data.current.hostel_name}
          </p>
          <p className="font-display text-4xl font-semibold mb-4">
            Room {data.current.room_number}
            <span className="text-lg text-ink-soft font-sans font-normal ml-2">
              · Bed {data.current.bed_number}
            </span>
          </p>
          <dl className="grid grid-cols-2 gap-4 text-sm border-t border-border pt-4">
            <div>
              <dt className="text-ink-soft">Room type</dt>
              <dd className="font-medium mt-0.5">{data.current.room_type}</dd>
            </div>
            <div>
              <dt className="text-ink-soft">Monthly rate</dt>
              <dd className="font-mono font-medium mt-0.5">${data.current.price}</dd>
            </div>
            <div>
              <dt className="text-ink-soft">Checked in</dt>
              <dd className="font-mono font-medium mt-0.5">{data.current.check_in_date}</dd>
            </div>
          </dl>
        </div>
      ) : (
        <div className="card p-10 text-center text-sm text-ink-soft max-w-lg">
          You don't have an active room assignment yet. Check with your hostel manager.
        </div>
      )}

      {data?.history?.length > 0 && (
        <div className="mt-8">
          <h2 className="font-display text-lg font-semibold mb-3">Past stays</h2>
          <div className="card divide-y divide-border">
            {data.history.map((stay) => (
              <div key={stay.id} className="p-4 flex justify-between text-sm">
                <span>{stay.hostel_name} — Room {stay.room_number}</span>
                <span className="font-mono text-ink-soft">
                  {stay.check_in_date} → {stay.check_out_date}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </Layout>
  );
}
