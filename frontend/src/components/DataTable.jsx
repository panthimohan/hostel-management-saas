/**
 * Responsive Data Table
 * - Fits dashboard width
 * - Horizontal scroll only when absolutely necessary
 * - Prevents pages from stretching wider than the viewport
 */

export default function DataTable({
  columns,
  rows,
  emptyLabel = "Nothing here yet.",
  rowKey = "id",
  loading = false,
}) {

  if (loading) {
    return (
      <div className="card p-10 text-center text-sm text-ink-soft">
        Loading...
      </div>
    );
  }

  if (!rows || rows.length === 0) {
    return (
      <div className="card p-10 text-center text-sm text-ink-soft">
        {emptyLabel}
      </div>
    );
  }

  return (
    <div className="card w-full overflow-hidden">
      <div className="w-full overflow-x-auto">
        <table className="w-full table-auto text-sm">
          <thead className="bg-fog">
            <tr className="border-b border-border">
              {columns.map((col) => (
                <th
                  key={col.key}
                  className="
                    px-4
                    py-3
                    text-left
                    text-xs
                    font-semibold
                    uppercase
                    tracking-wide
                    text-ink-soft
                    whitespace-nowrap
                  "
                >
                  {col.header}
                </th>
              ))}
            </tr>
          </thead>

          <tbody>
            {rows.map((row) => (
              <tr
                key={row[rowKey]}
                className="
                  border-b
                  border-border
                  hover:bg-fog/50
                  last:border-0
                "
              >
                {columns.map((col) => (
                  <td
                    key={col.key}
                    className={`
                      px-4
                      py-3
                      align-middle
                      break-words
                      ${col.mono ? "font-mono" : ""}
                      ${col.className || ""}
                    `}
                  >
                    {col.render
                      ? col.render(row)
                      : row[col.key] ?? "—"}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>

        </table>
      </div>
    </div>
  );
}