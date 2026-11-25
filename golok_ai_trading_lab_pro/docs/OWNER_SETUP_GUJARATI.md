# Golok AI Trading Lab Pro ચલાવવાની રીત

P09.1માં administrator **Prospective Fixture Paper Accounts**માં એક અથવા વધુ **Automated Fixture Research Schedules** પસંદ કરી શકે છે. તેની સાથે strategy, target policy અને hypothetical tariff પસંદ કરો. યોગ્ય બનાવટી signal મળે ત્યારે reservation આપમેળે થશે. એક જ ખાતાની schedules એક capital balance વાપરે છે અને એક સમયે એક જ exposure મંજૂર છે. નવા completed candles મળતાં **Orders and Positions** તથા **Journal (paise)**માં પરિણામ દેખાશે. **Fixture Risk Monitor**માં બાકી દૈનિક risk budget જુઓ. આ પ્રવાહ માટે Odoo અને સ્થાનિક scheduler ચાલુ હોવા જોઈએ.

P09માં **Research Schedules**માં fixture dataset પસંદ કરો અને 2થી 60 મિનિટનો interval સેટ કરો. નવો completed candle ઉપલબ્ધ થાય ત્યારે **Fixture Research Cycles**માં cutoff, jobની સ્થિતિ અને research fingerprint જુઓ. આ ચક્રનો પરિણામ **NO TRADE** છે.

**Prospective Fixture Paper Accounts**માં Risk Manager એક hypothetical tariff અને scenario પસંદ કરી ખાતું બનાવી શકે છે. **Reserve Fixture Order**, **Process Fixture Entry** અને **Process Fixture Exit** અનુક્રમે ચલાવો. **Journal (paise)**માં virtual cash અને riskના ફેરફારો જુઓ. **Pause and Cancel Pending Entries** બાકી reservation છોડે છે. આ બનાવટી workflowમાં broker જોડાતો નથી.

**Synthetic Portfolios**માં અગાઉનો synthetic replay ખોલીને **Calculate Performance** દબાવો. રિપોર્ટમાં net expectancy, fees અને બે અલગ drawdown ગણતરી દેખાય છે. શૂન્ય trades હોય ત્યારે પુરાવો અપૂરતો દેખાય છે.

**Run Walk-forward Experiment**માં training, validation, evaluation અને embargo માટે trading sessionsની સંખ્યા આપો. **Synthetic Walk-forward Experiments**માં દરેક foldની પસંદગી અને તેના પુરાવા જુઓ.

P08માં **Research Schedules** ખોલીને fixture calendar ધરાવતો dataset પસંદ કરો. **Check Session Now** હાલની સ્થિતિ નોંધે છે. **Daily Research Operations**માં તબક્કો, observations અને **NO TRADE**નું કારણ જુઓ. Laptop બંધ હોય ત્યારે સ્થાનિક scheduler ચાલતો નથી. ફરી ચાલુ થાય ત્યારે છેલ્લા ચેક પછીના છેલ્લાં સાત દિવસમાં પૂર્ણ થયેલાં સત્રોના post-market reports પુનઃબનાવી શકે છે. તેમાં **historical recovery** દેખાય છે.

અધિકૃત daily ફાઇલ આયાત કર્યા પછી **Normalize to Research Datasets** દબાવો. તારીખને આવરી લેતું NSE instrument mapping અને મેળ ખાતો ISIN હોવો જોઈએ. વાસ્તવિક CSV માટે **Source Authorizations**માં ચોક્કસ publisher અને ઉપયોગની મંજૂરી નોંધો.

મંજૂરીમાં સંગ્રહની છેલ્લી તારીખ હોય તો **Fixed-term storage** પસંદ કરીને તારીખ નોંધો. મુદત પૂરી થયા પછી datasetનો ઉપયોગ અટકે છે. **Compare Sources**માં એક જ instrument અને સમયની બે observations સરખાવી શકો છો. ગંભીર તફાવત મળે તો નવું research અને replay અટકે છે.

પોતે બનાવેલો synthetic dataset મેળવવા **Exchange Calendars**માં પૂર્ણ થયેલા fixture sessions ધરાવતું calendar ખોલીને **Generate Deterministic Fixture** દબાવો. Datasetમાં generatorનું version, seed અને SHA-256 દેખાશે. આ માટે broker account જરૂરી નથી.

P07માં **Completed market structure** મૂળ target પદ્ધતિ છે. યોગ્ય target ન મળે તો નિર્ણય **NO TRADE** રહે છે. અગાઉના synthetic પરિણામ સાથે સરખાવવા **Fixed 4R benchmark** પસંદ કરી શકો છો. વાસ્તવિક market CSV આયાત પહેલાં **Source Authorizations**માં સક્રિય પરવાનગી નોંધો.

Publisher સુધારેલી દૈનિક ફાઇલ આપે ત્યારે **End-of-day File Imports**માં **Previous File Revision** અને **Publisher Correction Reference** ભરો. Normalize કર્યા પછી સુધારેલી candles અલગ datasetમાં દેખાશે. **Run Synthetic Portfolio**માં server-generated dataset પસંદ કરીને **Test Historical Timing on Generated Fixtures** ચલાવી શકો છો. તેમાં મોડેલ કરેલું publication delay અને તેનો fingerprint સાચવાય છે.

વાસ્તવિક intraday replay માટે publisherની backtest પરવાનગી અને દરેક candleના પ્રકાશન સમયનો પુરાવો મેળવો. Administrator **Import historical CSV**માં મૂળ સંપૂર્ણ CSV અને પુરાવાની HTTPS લિંક આપીને **Verify Historical Publication** કરે. પછી યોગ્ય tariff પસંદ કરીને **Run Authorized Historical Replay** ચલાવો. વિગતવાર પગલાં [Owner actions](OWNER_ACTION_REQUIRED.md)માં છે.

1. તમારા સ્થાનિક Odoo 20નું સામાન્ય launcher ચાલુ કરો અને તેનો localhost સરનામો ખોલો. Appsમાં **Golok AI Trading Lab Pro** ઇન્સ્ટોલ અથવા અપગ્રેડ કરો. સક્રિય કંપની પસંદ કરો અને **Trading Lab → Research Overview** ખોલો.
2. બ્રોકર વગર અજમાવવા પોતાના બનાવેલા candles માટે **Synthetic fixture** પસંદ કરો. છેલ્લી candleનો સમય, importનો સમય અને data origin અલગથી વાંચો. દૈનિક Bhavcopy સત્ર પૂરું થયા પછીનો ડેટા છે.
3. **Source Authorizations**માં administrator સ્રોત, ઉપયોગ, શરતો, પુરાવો અને મંજૂરીની અંતિમ તારીખ નોંધે. ક્વેરી, ડિસ્પ્લે અને કાયમી આંતરિક સંગ્રહની મંજૂરી હોય ત્યારે જ તે અધિકારો પસંદ કરો. **End-of-day File Imports**માં સ્રોત, પૂરી થયેલી તારીખ અને NSE કૅલેન્ડર પસંદ કરીને ફાઇલ આપો. **Quarantined** દેખાય તો તારીખ, format અને ભાવ ચકાસો.
4. **Run Synthetic Portfolio**માં અલગ instrumentsના datasets, તારીખો અને hypothetical tariff પસંદ કરો. એક strategy માટે replay ચલાવો અથવા **Compare Five Strategies** દબાવો. **Walk-forward Validation** માટે ચારથી નવ તારીખનું આવરણ જરૂરી છે.
5. અંતિમ holdout માટે અગાઉનો training replay પસંદ કરો, અલગ તારીખો આપો અને **Seal Final Holdout** દબાવો. Risk Manager **Sealed Holdouts**માંથી તેને એક વખત ચલાવી શકે છે.
6. **Virtual replay accounts**માં ઐતિહાસિક simulated postings દેખાય છે. **NO TRADE** એટલે જરૂરી પુરાવા અથવા પરવાનગીના અભાવે કોઈ વ્યવહારયોગ્ય signal આપવામાં આવ્યો નથી. આ આવૃત્તિમાં ચકાસેલું live feed કે prospective paper performance ઉપલબ્ધ નથી.
7. હોટસ્પોટ બંધ થાય તો offline પરીક્ષણ ચાલુ રાખી શકો છો. બ્રોકર માટે **Sync History**માં કારણ જુઓ. કનેક્શન અને પરવાનગી પાછાં મળે ત્યાર પછી **Historical Sync Plans**માં આગળનું સત્ર ચલાવો. જૂના ભાવને live quote તરીકે વાપરશો નહીં.

હાલના offline અભ્યાસ માટે બહારનું ખાતું, static IP કે subscription લેવાની જરૂર નથી. વાસ્તવિક ડેટા માટે સંબંધિત સ્રોતના ઉપયોગ અને સંગ્રહની મંજૂરી જરૂરી છે.
## P06P07-R01 માં Upstox historical sync

**Trading Lab → Market Data API Configuration**માં Provider પહેલાં **Offline** છે. અસલી data માટે **Market Data Authorization**, reviewed NSE mapping અને calendar પસંદ કરીને **Apply Settings** દબાવો. **Set or Replace Analytics Token**માં token અને timezone સહિત તેની expiry દાખલ કરો. Token Windows પર સ્થાનિક રીતે encrypt થાય છે. તેને ચેટ કે review ZIPમાં મૂકવાની જરૂર નથી.

**Save and Test Connection** પસંદ કરેલી પરવાનગી મુજબ read-only ટેસ્ટ કરે છે. **Synchronize Instrument Reference** mapping ચકાસે છે. મંજૂર historical plan માટે **Automatically advance permitted historical plans** ચાલુ કરી શકો. મંજૂરી હોય ત્યારે V3 samples માટે **Collect timestamped V3 samples** પસંદ કરો. મોડા અથવા મંજૂરી વગરના samples છુપાય છે. અસલી feed અને paper-trading પરિણામોની ચકાસણી બાકી છે. [સંપૂર્ણ સેટઅપ](UPSTOX_ANALYTICS_CONFIGURATION.md)

**Synchronize Instrument Reference** મંજૂર NSE cash-equity catalogનું નવું સંસ્કરણ સાચવે છે. **Instrument Catalog**માં symbol અથવા ISINથી શોધો. Mappingમાં ફેરફાર માટે અલગ review જરૂરી છે.

1. Offline ચકાસણી માટે Trading System Administrator તરીકે Odooમાં NSE fixture calendar અને Upstox mapping બનાવો. Mappingની key `NSE_EQ|ISIN` સ્વરૂપમાં હોવી જોઈએ.
2. **Synchronize Historical** ખોલીને **Synthetic fixture** પસંદ કરો. Upstox V3નું synthetic JSON અને પૂર્ણ fixture session આપો. **Historical Sync Plans** માં `mapping_id/YYYY-MM-DD` key હેઠળ એ જ V3 response object આપી **Process Next Session** દબાવી શકો. **Sync History** માં count અને status જુઓ.
3. અસલી data માટે Upstox accountમાંથી Analytics Tokenની ઉપલબ્ધતા અને query, display, local storage તથા internal researchની લેખિત મંજૂરી ચકાસો. **Market Data Authorization** માં મંજૂરીની નોંધ કરો.
4. મંજૂરી મળ્યા પછી reviewed mapping અને calendar વાપરો. સ્થાનિક Odoo workerના environmentમાં token masked promptથી દાખલ કરો અને explicit authorization setting સક્રિય કરો. પ્રક્રિયા પછી token સ્થાનિક જ રાખો.
5. **Provider Diagnostics → Check Upstox Readiness** માં local setup, company authorization અને છેલ્લું સફળ અસલી receipt જુઓ.
6. Historical portfolio wizardમાં **Experimental causal entry, stop and target** પસંદ કરીને synthetic replay ચલાવો. પરિણામમાં signal સમયે નક્કી થયેલી entry range, stop, target અને veto જુઓ. એ જ policy સાથે **Run Walk-forward Experiment** દબાવો તો દરેક training foldમાં 20 strategy–policy જોડીઓ ચકાસાશે. અસલી market data અને નફાકારકતાની ચકાસણી બાકી છે.
7. બંને brokers માટે એ જ ISIN અને સત્રની reviewed mappings તથા raw OHLCV આયાત કરવાની સક્રિય મંજૂરી હોય તો **Synchronize Historical → Authorized Alternate**માં બીજું mapping પસંદ કરી શકો. મુખ્ય provider પર કામચલાઉ ભૂલ આવે ત્યારે એક વાર alternate અજમાવાશે. બંને પ્રયાસો **Sync History**માં જોડાયેલા રહેશે.

## Prospective fixture competition

**Fixture Candidate Research → Timing and Freshness**માં candleનો સમય, બનાવટી publication availability, સ્થાનિક receipt, cutoff અને entry expiry અલગ દેખાય છે. **Research History → Open Stock Chart** પસંદ કરેલા snapshotના cutoff પર EMA 20, SMA 20 અને ઉપલબ્ધ હોય ત્યારે session VWAP બતાવે છે.

**Daily Research Operations**માં કોઈ session event ખોલીને તે કંપની અને તારીખનો **Daily Research Report** જુઓ. તેમાં સાચવેલા phases, coverage, strategy trials, candidateનાં કારણો, risk vetoes અને બંધ થયેલા virtual ordersનું પરિણામ દેખાય છે. બંધ થયેલો order ઉપલબ્ધ ન હોય તો realized net માટે **Unavailable** દેખાય છે.

**Prospective Fixture Paper Accounts** માં અલગ instrumentsની synthetic schedules જોડો. Strategyમાં **Compete across all five strategies** પસંદ કરો. સમાન cutoffના jobs પૂરા થાય પછી યોગ્ય candidates સરખાવવામાં આવે છે અને accountમાંથી એક virtual reservation થાય છે. Expired candidate માટે reservation થતું નથી.

**Fixture Candidate Research** માં instrument, observation, entry, stop, target, rank અને rejectionનું કારણ જુઓ. **Provider Diagnostics → Review Provider Status** માં companyની મંજૂરી, retention અને historical receipt જુદાં દેખાય છે.

## Data conflict review

મંજૂરીવાળા સ્થાનિક CSVને import કર્યા પછી administrator એ જ પૂર્ણ CSV સાથે **Verify Comparison Source** પસંદ કરી શકે છે. Dataset raw OHLCV હોવું જોઈએ અને exchange calendar તથા ISIN mapping ચકાસેલા હોવા જોઈએ. આ પગલાથી comparison માટે dataset સાચવાઈ જાય છે.

**Compare Sources** માં મતભેદનું કારણ જુઓ. સુધારેલો dataset અને એ જ candle માટે સ્વતંત્ર sourceની પુષ્ટિ હોય ત્યારે **Record Corroborated Replacement** વાપરો. જૂના datasets અને audit નોંધ જળવાય છે.

**Run Walk-forward Experiment** માં experimental causal policy પસંદ કરીને **Fit a target cap on training observations** ચાલુ કરી શકો. Reportમાં training તારીખો, sample count અને લાગુ target cap દેખાય છે. Research snapshotમાં **Research Evidence Contract** દરેક capabilityનું પરિણામ અથવા ખૂટતો input બતાવે છે.

