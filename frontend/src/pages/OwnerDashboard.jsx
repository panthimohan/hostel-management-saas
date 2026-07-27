import { useEffect, useState } from "react";
import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";

import client from "../api/client";
import Layout from "../components/Layout";
import StatCard from "../components/StatCard";

const CHART_COLORS = [
  "#145C5A",
  "#C98A2C",
  "#3F7A5D",
  "#B3492E",
  "#1E7A76",
  "#E0A94E",
  "#4B5D62",
  "#0D423F",
  "#A96E1B",
  "#DDE3E0"
];

export default function OwnerDashboard() {
  const [hostels, setHostels] = useState([]);
  const [rooms, setRooms] = useState([]);
  const [beds, setBeds] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  async function load() {
    try {
      const [hostelsRes, roomsRes, bedsRes, summaryRes] = await Promise.all([
        client.get("/hostels/"),
        client.get("/rooms/"),
        client.get("/beds/"),
        client.get("/expenses/summary/"),
      ]);

      setHostels(hostelsRes.data.results ?? hostelsRes.data);
      setRooms(roomsRes.data.results ?? roomsRes.data);
      setBeds(bedsRes.data.results ?? bedsRes.data);
      setSummary(summaryRes.data);
    } finally {
      setLoading(false);
    }
  }

    useEffect(() => {
    load();

    const refresh = () => load();

    window.addEventListener("dashboard-refresh", refresh);

    return () => {
      window.removeEventListener("dashboard-refresh", refresh);
    };
  }, []);
  const vacantBeds = beds.filter((b) => b.status === "VACANT").length;
  const occupiedBeds = beds.filter((b) => b.status === "OCCUPIED").length;

  const occupancyRate = beds.length
    ? Math.round((occupiedBeds / beds.length) * 100)
    : 0;


  // occupancy calculation per hostel
  const hostelOccupancy = hostels.map((hostel) => {
    const hostelRooms = rooms.filter(
      (room) => room.hostel === hostel.id
    );

    const hostelBeds = beds.filter((bed) =>
      hostelRooms.some((room) => room.id === bed.room)
    );

    const occupied = hostelBeds.filter(
      (bed) => bed.status === "OCCUPIED"
    ).length;

    return {
      name: hostel.name,
      occupied,
      total: hostelBeds.length,
      percentage: hostelBeds.length
        ? Math.round((occupied / hostelBeds.length) * 100)
        : 0,
    };
  });


  return (
    <Layout>

      <div className="mb-6">
        <h1 className="font-display text-2xl font-semibold">
          Dashboard
        </h1>

        <p className="text-sm text-ink-soft mt-1">
          A snapshot of your hostel business, right now.
        </p>
      </div>


      {loading ? (
        <div className="card p-10 text-center text-sm text-ink-soft">
          Loading your dashboard…
        </div>
      ) : (

        <>

          {/* KPI CARDS */}
          <div className="grid grid-cols-2 lg:grid-cols-5 gap-4 mb-6">

            <StatCard
              label="Hostels"
              value={hostels.length}
            />

            <StatCard
              label="Rooms"
              value={rooms.length}
            />

            <StatCard
              label="Total Beds"
              value={beds.length}
            />

            <StatCard
              label="Occupied Beds"
              value={occupiedBeds}
              hint={`${occupancyRate}% occupancy`}
              tone="moss"
            />

            <StatCard
              label="Expenses"
              value={`$${Number(summary?.total || 0).toLocaleString()}`}
              tone="clay"
            />

          </div>



          <div className="grid lg:grid-cols-5 gap-6">


            {/* BED STATUS */}
            <div className="card p-5 lg:col-span-2">

              <h2 className="font-display text-lg font-semibold mb-4">
                Beds at a glance
              </h2>


              <div className="space-y-3">

                <BedRow
                  label="Vacant"
                  count={vacantBeds}
                  total={beds.length}
                  tone="moss"
                />


                <BedRow
                  label="Occupied"
                  count={occupiedBeds}
                  total={beds.length}
                  tone="brass"
                />


                <BedRow
                  label="Reserved / Maintenance"
                  count={
                    beds.length -
                    vacantBeds -
                    occupiedBeds
                  }
                  total={beds.length}
                  tone="clay"
                />

              </div>

            </div>




            {/* HOSTEL OCCUPANCY */}
            <div className="card p-5 lg:col-span-3">

              <h2 className="font-display text-lg font-semibold mb-4">
                Occupancy by Hostel
              </h2>


              <div className="space-y-5">

                {hostelOccupancy.map((item)=>(
                  <div key={item.name}>

                    <div className="flex justify-between text-sm mb-2">

                      <span className="text-ink-soft">
                        {item.name}
                      </span>

                      <span className="font-mono">
                        {item.occupied}/{item.total}
                      </span>

                    </div>


                    <div className="h-3 bg-fog rounded-full overflow-hidden">

                      <div
                        className="h-full bg-moss rounded-full"
                        style={{
                          width:`${item.percentage}%`
                        }}
                      />

                    </div>


                    <p className="text-xs text-ink-soft mt-1">
                      {item.percentage}% occupied
                    </p>


                  </div>
                ))}


                {hostelOccupancy.length === 0 && (
                  <p className="text-sm text-ink-soft">
                    No hostel data available.
                  </p>
                )}

              </div>


            </div>




            {/* EXPENSE CHART */}
            <div className="card p-5 lg:col-span-5">

              <h2 className="font-display text-lg font-semibold mb-1">
                Expenses by category
              </h2>

              <p className="text-xs text-ink-soft mb-4">
                Includes Miscellaneous spend not covered elsewhere.
              </p>


              {summary?.by_category?.length ? (

                <div className="grid sm:grid-cols-2 gap-4 items-center">


                  <div className="h-56">

                    <ResponsiveContainer width="100%" height="100%">

                      <PieChart>

                        <Pie
                          data={summary.by_category}
                          dataKey="total"
                          nameKey="category_display"
                          innerRadius={50}
                          outerRadius={80}
                          paddingAngle={2}
                        >

                          {summary.by_category.map((entry,i)=>(

                            <Cell
                              key={entry.category}
                              fill={
                                CHART_COLORS[
                                  i % CHART_COLORS.length
                                ]
                              }
                            />

                          ))}

                        </Pie>


                        <Tooltip
                          formatter={(value)=>
                            `$${Number(value).toLocaleString()}`
                          }
                        />

                      </PieChart>

                    </ResponsiveContainer>

                  </div>


                </div>

              ) : (

                <p className="text-sm text-ink-soft py-8 text-center">
                  No expenses recorded yet.
                </p>

              )}

            </div>


          </div>

        </>
      )}

    </Layout>
  );
}



function BedRow({ label, count, total, tone }) {

  const pct = total
    ? Math.round((count / total) * 100)
    : 0;


  const barColor = {
    moss:"bg-moss",
    brass:"bg-brass",
    clay:"bg-clay"
  }[tone];


  return (

    <div>

      <div className="flex justify-between text-sm mb-1">

        <span className="text-ink-soft">
          {label}
        </span>

        <span className="font-mono font-medium">
          {count}
        </span>

      </div>


      <div className="h-2 rounded-full bg-fog overflow-hidden">

        <div
          className={`h-full ${barColor} rounded-full`}
          style={{
            width:`${pct}%`
          }}
        />

      </div>

    </div>

  );
}