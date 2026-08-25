import { useEffect, useState } from "react";

import { fetchDisagreements, fetchOrganizations } from "./apis/reconciliation";

import FilterBar from "./components/FilterBar";
import DisagreementTable from "./components/DisagreementTable";
import "./App.css";

export default function App() {
  const [organizations, setOrganizations] = useState([]);
  const [disagreements, setDisagreements] = useState([]);

  const [selectedOrganization, setSelectedOrganization] = useState("");

  const [selectedReason, setSelectedReason] = useState("");

  const [selectedSort, setSelectedSort] = useState("");

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadOrganizations() {
      try {
        const data = await fetchOrganizations();
        setOrganizations(data);
      } catch (error) {
        setError(error.message);
      }
    }

    loadOrganizations();
  }, []);

  useEffect(() => {
    async function loadDisagreements() {
      setLoading(true);
      setError("");

      try {
        const data = await fetchDisagreements({
          orgId: selectedOrganization,
          reason: selectedReason,
          sort: selectedSort,
        });

        setDisagreements(data);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    }

    loadDisagreements();
  }, [selectedOrganization, selectedReason, selectedSort]);

  return (
    <main className="app">
      <header>
        <h1>Record Reconciliation</h1>
        <p>Review disagreements between System A and System B.</p>
      </header>

      <FilterBar
        organizations={organizations}
        selectedOrganization={selectedOrganization}
        selectedReason={selectedReason}
        selectedSort={selectedSort}
        onOrganizationChange={setSelectedOrganization}
        onReasonChange={setSelectedReason}
        onSortChange={setSelectedSort}
      />

      {error && <p className="error">{error}</p>}

      {loading ? (
        <p>Loading disagreements...</p>
      ) : (
        <DisagreementTable disagreements={disagreements} />
      )}
    </main>
  );
}
