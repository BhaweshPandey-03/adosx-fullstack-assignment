# Engineering Decisions

## 1. Django + React

Decision:
Use Django for the backend and React for the frontend.

Alternative rejected:
Use a Node/Express backend since that is more familiar to me.

Reason:
The assignment prefers Django, and the project benefits from Django's ORM, migrations, and management commands for the data-import problem.

## 2. SQLite

Decision:
Use SQLite for the assignment database.

Alternative rejected:
Use PostgreSQL.

Reason:
The dataset is very small, and SQLite removes unnecessary database setup while still providing a proper relational database.

## 3. Preserve Raw CSV Data

Decision:
Store the original CSV row in `raw_data` alongside parsed fields.

Alternative rejected:
Store only normalized and parsed values.

Reason:
The brief requires dirty rows to survive import, and retaining the raw input makes the import behavior easier to inspect and debug.

## 4. Normalize Only System B References

Decision:
Treat System A's `record_id` as the canonical identifier and normalize System B's `record_ref`.

Alternative rejected:
Normalize identifiers from both systems.

Reason:
The inconsistent reference formats are present on the System B side, so only the B-side value needs normalization before matching.

## 5. Tenant-Aware Matching

Decision:
Match records using `(organization_id, record_id)`.

Alternative rejected:
Match records using `record_id` alone.

Reason:
The same record ID can appear under different organizations, and the assignment requires strict tenant isolation.

## 6. Preserve Duplicate System B Entries

Decision:
Keep every System B entry as a separate database row and use `entry_id` as the unique identifier for the entry.

Alternative rejected:
Use `record_ref` as the unique identifier for System B rows.

Reason:
Multiple System B entries for the same record are an explicit disagreement case, so they must be preserved rather than overwritten.

## 7. Reconciliation as a Separate Service

Decision:
Keep comparison logic in a dedicated reconciliation service.

Alternative rejected:
Implement the comparison directly inside the Django API view.

Reason:
The reconciliation rules are the main business logic and should be independently testable and reusable by the API.

## 8. Minimal UI

Decision:
Build a simple table with organization filtering, reason filtering, and value sorting.

Alternative rejected:
Build a dashboard-style interface with charts and additional controls.

Reason:
The assignment explicitly prioritizes correctness and functionality over visual design, so development time was focused on the data flow and reconciliation logic.