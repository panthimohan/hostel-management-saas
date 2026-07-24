export default function StatCard({ label, value, hint, tone = "default" }) {
  const toneClasses = {
    default: "text-ink",
    brass: "text-brass-dark",
    moss: "text-moss",
    clay: "text-clay",
  };
  return (
    <div className="card p-5 flex flex-col gap-1 min-w-0">
      <span className="text-xs font-semibold uppercase tracking-wide text-ink-soft">
        {label}
      </span>
      <span className={`font-display text-3xl font-semibold ${toneClasses[tone]} truncate`}>
        {value}
      </span>
      {hint && <span className="text-xs text-ink-soft">{hint}</span>}
    </div>
  );
}
