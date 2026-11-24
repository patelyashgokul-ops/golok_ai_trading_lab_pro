# P07 automation and recovery

The inherited Odoo research queue claims a queued job with transactional PostgreSQL row locking and deduplicates by company, dataset, cutoff and requester. Historical sync remains operator-triggered with persisted checkpoints. The local suite exercises the existing queue dispatch and cancellation plus independent transactions for portfolio holdout consumption and historical posting.

Session-aware pre-market, intraday and post-market orchestration, automatic prospective paper trading, forced process restart, lease recovery and hotspot interruption remain open. The release does not claim prospective operational history. [ORM tests](../tests/test_lab.py) · [Database contention script](../scripts/verify_contention.py)
