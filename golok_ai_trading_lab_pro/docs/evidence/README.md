# Evidence index

| Directory | Evidence |
|---|---|
| `tests/` | Standalone parser and descriptive-indicator tests |
| `installation/` | Odoo fresh-install and same-version upgrade logs. Failed iterations are preserved in the installation log. |
| `browser/` | Headless Edge verification output |
| `screenshots/` | Screenshots captured from the actual Odoo interface when rendering passed |
| `performance/` | Synthetic standalone service measurements |
| `security/` | Source scan. ORM security assertions are in installation logs. |
| `integration/` | No SmartAPI evidence. Authorized credentials and a read-only adapter were unavailable. |
| `quantitative/` | No financial experiment evidence. Reference calculation tests are in the unit log. |

The manifest lists SHA-256 hashes from the close of the development run. Install and browser logs contain only disposable test data. Database internals, session logs and test credentials are excluded.
