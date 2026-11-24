# P06–P07 strategy optimization

- RE-21 proposes tick-aligned signal, prior breakout and approximate VWAP limits using completed observations. **Experimental causal entry, stop and target** applies the evaluator to the five historical portfolio strategies. It freezes the proposal at signal time and checks the later open against its range, limit and expiry.
- RE-22 compares strategy invalidation, recent swing, ATR and volatility-buffer stops. The Decimal sizing service checks gap stress, hypothetical costs, liquidity, capital, tick size and the two-to-one minimum net reward-to-risk. The replay records the selected stop and simulated fill. Stops stay fixed through the simulated position.
- RE-23 adds **Experimental ATR-capped resistance** to historical portfolio replay. It uses the nearer completed resistance or two ATR above the entry, whichever is lower, with tick alignment in the replay. Insufficient volatility history or a missing defensible barrier yields no target. Published structure and fixed 4R benchmark policies retained their definitions and archived synthetic results.
- With the joint policy selected, **Run Walk-forward Experiment** evaluates 20 strategy–policy pairs per training fold. The same frozen strategy and policy carry through validation and, if eligible, evaluation. The report keeps zero-trade and losing training trials. Prospective competition, wider parameter calibration, historical excursion statistics and genuine performance remain open.

[Target policy comparison and strategy evidence](evidence/p06_p07_repair/INDEX.md)
