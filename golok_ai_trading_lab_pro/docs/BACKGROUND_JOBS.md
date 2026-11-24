# Historical research queue

The native queue stores company, dataset, requested cutoff, requester, result, terminal state and elapsed time. Equivalent submissions from the same requester are constrained to one row. The requester can cancel a queued row. The scheduled action starts disabled.

The worker processes one request per activation with a `FOR UPDATE SKIP LOCKED` claim. It runs research with the requesting user's current permissions and company. If interrupted before commit, the database rolls back both claim and output. Validation and revoked-access errors produce a sanitized failure. The queue has no broker fetches, backdating, daily orchestration, automatic paper fills or separately scheduled provider operations.
