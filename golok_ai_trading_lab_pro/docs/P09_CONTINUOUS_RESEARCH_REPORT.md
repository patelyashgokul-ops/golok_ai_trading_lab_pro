# P09 continuous fixture research

Session phase reports keep their original unique watch, date and phase key. A separate cycle references the current watch, company, dataset, newest eligible observation, publication time, cutoff and durable research job. Administrators configure a 2–60 minute minimum interval. The scheduler evaluates at most 32 watches and keeps at most one waiting or claimed job per watch and day. A watch row lock and observation uniqueness prevent duplicate concurrent scheduling. The P08 queue retains its committed lease and limited retries.

Newly available observations can schedule a cycle at the next cron check. A cycle compares the configured dataset and active schedule again at execution. The resulting descriptive findings, gate evidence and immutable input SHA-256 are published atomically with the result. A completed fixture outcome has NO TRADE status. An estimated missed-interval count accompanies newly queued work where a prior check is known. The existing seven-day historical post-market recovery remains available.

This implementation uses bounded sampling of the latest available observation. It does not enumerate every missed intraday slot or independently capture acquisition attempts. The recurrence path has no immediate upload hook or verified real-feed support. [Implementation](../models/session_ops.py)
