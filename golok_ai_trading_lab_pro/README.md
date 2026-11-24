# Golok AI Trading Lab Pro

P05 adds **Historical Sync Plans** for bounded, checkpointed ingestion and **Run Synthetic Portfolio** for shared virtual capital across multiple instruments. Portfolio records preserve the input hashes, fees and decision gates for ST-01, ST-02 and ST-08. Fixture mode works without a broker account. The owner guide covers local read-only setup for an authorized historical test. [Owner actions](docs/OWNER_ACTION_REQUIRED.md)

An Odoo 20 Community add-on for historical NSE and BSE equity research. P03 adds effective-dated reference records, split-session calendar validation, supplemental research, bounded synthetic ST-01 experiments in Odoo, and a virtual historical replay journal. Historical analytical snapshots remain **NO TRADE**.

## Install and use

1. Install Odoo 20 Community and PostgreSQL using the Odoo source distribution’s dependencies. The add-on needs no extra Python packages at runtime. Put the module directory on Odoo's `addons_path`, restart Odoo and update the Apps list.
2. Install **Golok AI Trading Lab Pro**. Assign a user the Trading System Administrator role to register instruments, Trading Research Analyst to import and run research, or Trading Research Viewer for read access. Use the intended active company. Users who want market time in native Odoo fields can select **Asia/Kolkata** in their preferences.
3. In **Trading Lab → Instruments**, register the NSE or BSE instrument. In **Datasets**, select the instrument, interval, origin and a source label that identifies the authorized file publication or revision. Choose **Synthetic fixture** for generated data.
4. In **Import CSV**, select the dataset and upload a UTF-8 file with the following header. The example uses a fictitious observation.

   ```csv
   close_time,open,high,low,close,volume
   2024-01-02T09:20:00+05:30,100,102,99,101,1000
   ```

   Use candle close times with an explicit time offset and zero seconds. Supply ascending, unique timestamps. Maximum upload is 512 KiB or 4,000 rows. An identical re-import adds zero duplicates. A conflicting observation requires a distinct source revision.
5. For point-in-time research, create an immutable revision in **Exchange Calendars** and select it when registering a new dataset. Follow the [calendar contract](docs/EXCHANGE_CALENDAR.md) to include explicit opening and publication times. Legacy datasets retain the six-column import and original research digest.
6. In **Run Research**, choose the dataset and a cutoff, then open the result. In **Overview**, use **Show historical chart** to display up to 60 observations from the latest intact snapshot. Company counts, ingestion time, quarantine status and the research-only decision are server-backed.

Run the synthetic [ST-01 replay](docs/BACKTEST_EXECUTION_POLICY.md) with the provided fixture:

```powershell
python -B scripts/run_backtest.py tests/fixtures/p02/spec.json tests/fixtures/p02/candles.csv
```

Trading Risk Managers can create **Virtual Accounts** and use **Post Replay** to post a completed synthetic experiment. Prospective simulation and real trading are disabled. See the [owner quick start](docs/OWNER_QUICK_START.md) and [virtual accounting policy](docs/PAPER_LEDGER_INVARIANTS.md).

The [SmartAPI diagnostics](docs/SMARTAPI_SETUP.md) are offline by default. Authorized broker verification is pending.

## Verify

P03 uses PostgreSQL's bundled `btree_gist` extension for effective-date constraints. The Odoo database role must be able to create this trusted extension in the database, or the database administrator can install it beforehand.

Run `python -B -m unittest discover -s tests -p "unit_*.py" -v` from the add-on root. On Windows, run `./scripts/verify_odoo.ps1` for disposable verification. Add `-Browser` for Playwright and Edge. Run the harness directly and avoid piping the entire script. The parameterized `scripts/verify_p01_upgrade.ps1` clones a disposable populated database as its migration target.

See [Development report](DEVELOPMENT_REPORT.md) and [architecture](docs/ARCHITECTURE.md).
