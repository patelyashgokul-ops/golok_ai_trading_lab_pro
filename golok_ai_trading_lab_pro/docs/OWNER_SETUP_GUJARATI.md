# Golok AI Trading Lab Pro ચલાવવાની રીત

P08માં **Research Schedules** ખોલીને fixture calendar ધરાવતો dataset પસંદ કરો. **Check Session Now** હાલની સ્થિતિ નોંધે છે. **Daily Research Operations**માં તબક્કો, observations અને **NO TRADE**નું કારણ જુઓ. Laptop બંધ હોય ત્યારે સ્થાનિક scheduler ચાલતો નથી. ફરી ચાલુ થાય ત્યારે છેલ્લા ચેક પછીના છેલ્લાં સાત દિવસમાં પૂર્ણ થયેલાં સત્રોના post-market reports પુનઃબનાવી શકે છે. તેમાં **historical recovery** દેખાય છે.

અધિકૃત daily ફાઇલ આયાત કર્યા પછી **Normalize to Research Datasets** દબાવો. તારીખને આવરી લેતું NSE instrument mapping અને મેળ ખાતો ISIN હોવો જોઈએ. વાસ્તવિક CSV માટે **Source Authorizations**માં ચોક્કસ publisher અને ઉપયોગની મંજૂરી નોંધો.

મંજૂરીમાં સંગ્રહની છેલ્લી તારીખ હોય તો **Fixed-term storage** પસંદ કરીને તારીખ નોંધો. મુદત પૂરી થયા પછી datasetનો ઉપયોગ અટકે છે. **Compare Sources**માં એક જ instrument અને સમયની બે observations સરખાવી શકો છો. ગંભીર તફાવત મળે તો નવું research અને replay અટકે છે.

પોતે બનાવેલો synthetic dataset મેળવવા **Exchange Calendars**માં પૂર્ણ થયેલા fixture sessions ધરાવતું calendar ખોલીને **Generate Deterministic Fixture** દબાવો. Datasetમાં generatorનું version, seed અને SHA-256 દેખાશે. આ માટે broker account જરૂરી નથી.

P07માં **Completed market structure** મૂળ target પદ્ધતિ છે. યોગ્ય target ન મળે તો નિર્ણય **NO TRADE** રહે છે. અગાઉના synthetic પરિણામ સાથે સરખાવવા **Fixed 4R benchmark** પસંદ કરી શકો છો. વાસ્તવિક market CSV આયાત પહેલાં **Source Authorizations**માં સક્રિય પરવાનગી નોંધો.

Publisher સુધારેલી દૈનિક ફાઇલ આપે ત્યારે **End-of-day File Imports**માં **Previous File Revision** અને **Publisher Correction Reference** ભરો. Normalize કર્યા પછી સુધારેલી candles અલગ datasetમાં દેખાશે. **Run Synthetic Portfolio**માં server-generated dataset પસંદ કરીને **Test Historical Timing on Generated Fixtures** ચલાવી શકો છો. તેમાં મોડેલ કરેલું publication delay અને તેનો fingerprint સાચવાય છે.

1. તમારા સ્થાનિક Odoo 20નું સામાન્ય launcher ચાલુ કરો અને તેનો localhost સરનામો ખોલો. Appsમાં **Golok AI Trading Lab Pro** ઇન્સ્ટોલ અથવા અપગ્રેડ કરો. સક્રિય કંપની પસંદ કરો અને **Trading Lab → Research Overview** ખોલો.
2. બ્રોકર વગર અજમાવવા પોતાના બનાવેલા candles માટે **Synthetic fixture** પસંદ કરો. છેલ્લી candleનો સમય, importનો સમય અને data origin અલગથી વાંચો. દૈનિક Bhavcopy સત્ર પૂરું થયા પછીનો ડેટા છે.
3. **Source Authorizations**માં administrator સ્રોત, ઉપયોગ, શરતો, પુરાવો અને મંજૂરીની અંતિમ તારીખ નોંધે. ક્વેરી, ડિસ્પ્લે અને કાયમી આંતરિક સંગ્રહની મંજૂરી હોય ત્યારે જ તે અધિકારો પસંદ કરો. **End-of-day File Imports**માં સ્રોત, પૂરી થયેલી તારીખ અને NSE કૅલેન્ડર પસંદ કરીને ફાઇલ આપો. **Quarantined** દેખાય તો તારીખ, format અને ભાવ ચકાસો.
4. **Run Synthetic Portfolio**માં અલગ instrumentsના datasets, તારીખો અને hypothetical tariff પસંદ કરો. એક strategy માટે replay ચલાવો અથવા **Compare Five Strategies** દબાવો. **Walk-forward Validation** માટે ચારથી નવ તારીખનું આવરણ જરૂરી છે.
5. અંતિમ holdout માટે અગાઉનો training replay પસંદ કરો, અલગ તારીખો આપો અને **Seal Final Holdout** દબાવો. Risk Manager **Sealed Holdouts**માંથી તેને એક વખત ચલાવી શકે છે.
6. **Virtual replay accounts**માં ઐતિહાસિક simulated postings દેખાય છે. **NO TRADE** એટલે જરૂરી પુરાવા અથવા પરવાનગીના અભાવે કોઈ વ્યવહારયોગ્ય signal આપવામાં આવ્યો નથી. આ આવૃત્તિમાં ચકાસેલું live feed કે prospective paper performance ઉપલબ્ધ નથી.
7. હોટસ્પોટ બંધ થાય તો offline પરીક્ષણ ચાલુ રાખી શકો છો. બ્રોકર માટે **Sync History**માં કારણ જુઓ. કનેક્શન અને પરવાનગી પાછાં મળે ત્યાર પછી **Historical Sync Plans**માં આગળનું સત્ર ચલાવો. જૂના ભાવને live quote તરીકે વાપરશો નહીં.

હાલના offline અભ્યાસ માટે બહારનું ખાતું, static IP કે subscription લેવાની જરૂર નથી. વાસ્તવિક ડેટા માટે સંબંધિત સ્રોતના ઉપયોગ અને સંગ્રહની મંજૂરી જરૂરી છે.
