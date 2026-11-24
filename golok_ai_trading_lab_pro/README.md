# Golok AI Trading Lab Pro

An Odoo 20 Community add-on for historical NSE and BSE equity research. This milestone imports historical or synthetic OHLCV, stores validated candles, computes descriptive research and displays a database-backed overview. Each snapshot has a historical **NO TRADE** decision.

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
5. In **Run Research**, choose the dataset and a cutoff, then open the result. The overview shows counts and the latest snapshot for the active company. SMA(20), relative volume and ATR(14) appear when their required inputs are available.

Paper account setup and SmartAPI connection are pending implementation.

## Verify

Run `python -B -m unittest discover -s tests -p "unit_*.py" -v` from the add-on root. On Windows, run `./scripts/verify_odoo.ps1` with the appropriate path parameters for the disposable PostgreSQL cluster and Odoo stack. Add `-Browser` to exercise the real workflow using Playwright and installed Edge. The harness binds temporary services to loopback and stops them after the run. Allow localhost connections and headless browser process creation in restricted environments.

See [Development report](DEVELOPMENT_REPORT.md) and [architecture](docs/ARCHITECTURE.md).
