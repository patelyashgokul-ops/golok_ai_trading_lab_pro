# P03 resource limits

The CSV importer accepts up to 512 KiB and 4,000 rows. Research snapshots read up to 250 bars; chart responses return up to 60. One historical queue action handles one request. Synthetic replay limits are one instrument, 31 calendar dates and 4,000 bars. Authentication diagnostics are paced locally through PostgreSQL.

The isolated Odoo workload exercised 50 synthetic instruments and 3,750 bars. It measures server-side parsing, database writes and research with process and available-memory readings. It does not establish live feed capacity or browser latency. See [measurement](evidence/p03/migration/performance/orm.json).
