const API_BASE_URL = "http://127.0.0.1:8000/api";

export async function fetchOrganizations() {
  const response = await fetch(`${API_BASE_URL}/orgs/`);

  if (!response.ok) {
    throw new Error("Failed to load organizations");
  }

  return response.json();
}

export async function fetchDisagreements({ orgId, reason, sort } = {}) {
  const params = new URLSearchParams();

  if (orgId) {
    params.set("org_id", orgId);
  }

  if (reason) {
    params.set("reason", reason);
  }

  if (sort) {
    params.set("sort", sort);
  }

  const query = params.toString();

  const url = query
    ? `${API_BASE_URL}/disagreements/?${query}`
    : `${API_BASE_URL}/disagreements/`;

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error("Failed to load disagreements");
  }

  return response.json();
}
