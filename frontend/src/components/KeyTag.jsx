const VARIANT_MAP = {
  // room / bed statuses
  AVAILABLE: "available",
  VACANT: "available",
  OCCUPIED: "occupied",
  FULL: "full",
  RESERVED: "reserved",
  MAINTENANCE: "maintenance",
  CLOSED: "closed",
  // organization statuses
  PENDING: "pending",
  ACTIVE: "active",
  SUSPENDED: "suspended",
  CANCELLED: "cancelled",
};

/**
 * Signature status badge shaped like a physical hostel room-key fob:
 * a pill with a small punched hole at the left edge.
 * `surface` controls whether the punched hole matches a white card
 * background or the page's fog background.
 */
export default function KeyTag({ status, label, surface = true }) {
  const variant = VARIANT_MAP[status] || "neutral";
  return (
    <span
      className={`key-tag key-tag--${variant} ${surface ? "key-tag--surface" : ""}`}
    >
      {label || status?.replace(/_/g, " ")}
    </span>
  );
}
