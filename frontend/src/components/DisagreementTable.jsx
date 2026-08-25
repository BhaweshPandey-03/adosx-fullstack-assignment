function formatReason(reason) {
  return reason
    .replaceAll("_", " ")
    .toLowerCase()
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

function formatValue(value) {
  if (value === null || value === undefined) {
    return "—";
  }

  return value;
}

export default function DisagreementTable({ disagreements }) {
  if (disagreements.length === 0) {
    return <p>No disagreements found.</p>;
  }

  return (
    <table>
      <thead>
        <tr>
          <th>Reason</th>
          <th>Record</th>
          <th>Organization</th>
          <th>Location</th>
          <th>System A</th>
          <th>System B</th>
        </tr>
      </thead>

      <tbody>
        {disagreements.map((item) => (
          <tr key={`${item.reason}-${item.org_id}-${item.record_id}`}>
            <td>{formatReason(item.reason)}</td>
            <td>{item.record_id}</td>
            <td>{item.org_id}</td>
            <td>{item.location_id}</td>
            <td>{formatValue(item.system_a_value)}</td>
            <td>{formatValue(item.system_b_value)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
