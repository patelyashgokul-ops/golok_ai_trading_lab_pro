# P03 security

P04 adds administrator-only synchronization and read-only company-scoped audit rows. Direct dataset and CSV writes cannot originate provider observations. A real request must be explicitly enabled in the local process and has an operation-specific database reservation. Sync errors are sanitized before saving; tokens never enter model fields.

Native `ir.access` groups and global company filters govern new models. System Administrators maintain calendars and reference data and invoke provider diagnostics. Risk Managers record hypothetical fees, create virtual accounts and post synthetic replay. Analysts start research and synthetic experiments. Viewer access is read-only. Generated result or cash fields are rejected as user input, and manually callable methods check authorization before idempotent returns.

Only the virtual-account command writes journal events and balance with scoped elevation, within one PostgreSQL transaction. Jobs impersonate their requester. Provider requests use the existing three fixed HTTPS operations. No Odoo route places real orders or writes to the Odoo accounting ledger.
