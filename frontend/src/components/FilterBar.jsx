const REASONS = [
  "MISSING_IN_B",
  "ORPHAN_IN_B",
  "DUPLICATE_IN_B",
  "VALUE_MISMATCH",
];

function formatReason(reason) {
  return reason
    .replaceAll("_", " ")
    .toLowerCase()
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

export default function FilterBar({
  organizations,
  selectedOrganization,
  selectedReason,
  selectedSort,
  onOrganizationChange,
  onReasonChange,
  onSortChange,
}) {
  return (
    <div className="filter-bar">
      <label>
        Organization
        <select
          value={selectedOrganization}
          onChange={(event) => onOrganizationChange(event.target.value)}
        >
          <option value="">All organizations</option>

          {organizations.map((organization) => (
            <option key={organization.org_id} value={organization.org_id}>
              {organization.org_id}
            </option>
          ))}
        </select>
      </label>

      <label>
        Reason
        <select
          value={selectedReason}
          onChange={(event) => onReasonChange(event.target.value)}
        >
          <option value="">All reasons</option>

          {REASONS.map((reason) => (
            <option key={reason} value={reason}>
              {formatReason(reason)}
            </option>
          ))}
        </select>
      </label>

      <label>
        Sort
        <select
          value={selectedSort}
          onChange={(event) => onSortChange(event.target.value)}
        >
          <option value="">Default</option>
          <option value="value_asc">Value: low to high</option>
          <option value="value_desc">Value: high to low</option>
        </select>
      </label>
    </div>
  );
}
